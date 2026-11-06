"""Günlük çalışma ve tarihsel tamamlama.

Akış: topla → tekilleştir → sınıflandır → (yüksek güven) kalıcı backlog → öncelik sırasıyla arşivle.
Bütçeye sığmayan hiçbir kayıt kaybolmaz: backlog'da bekler ya da kimliği defterde (ledger) saklanır.
Her sayfa işlendikten sonra durum diske yazılır; çalışma kesilirse aynı gün/sayfadan devam edilir.
Arşiv, backlog ve inceleme kuyruğu aynı çalışmayı tekrar eklemez; bu yüzden yeniden işleme güvenlidir.
"""
import math
import time
import traceback
from datetime import date, timedelta

import kb

from . import records as R
from .archive import Archive, ReviewQueue
from .backlog import Backlog, Ledger, entry_key
from .classify import Classifier, llm_classify
from .discovery import Discovery
from .http import SourceUnavailable
from .llm import LLMUnavailable, BudgetExceeded, LLMError
from . import maintainer as M
from .sources import arxiv, crossref, openalex
from .state import State, daterange, parse_date, load_json, save_json

OPENALEX_STREAMS = ("journal", "biorxiv-medrxiv")


class Run:
    def __init__(self, cfg, http, llm=None, sources=("arxiv", "openalex"), log=print):
        self.cfg, self.http, self.log = cfg, http, log
        self.state = State(cfg.state_dir, cfg.today)
        self.counter = self.state.day_counter()
        self.tree = kb.Tree()
        self.clf = Classifier(self.tree)
        self.archive = Archive(self.tree, cfg.today)
        self.ledger = Ledger(cfg.state_dir, cfg.today)
        self.backlog = Backlog(cfg, self.ledger)
        self.queue = ReviewQueue(cfg.review_dir, cfg.review_queue_max, self.ledger, cfg.review_expire_days)
        self.discovery = Discovery(cfg, self.tree, self.clf)
        self.llm = llm
        self.sources = sources
        self.mem = {}  # bu çalışmada çekilen kayıtlar: backlog'dan arşivlerken yeniden çekmeye gerek kalmaz
        self.stats = {"fetched": 0, "skipped_seen": 0, "skipped_known": 0,
                      "classified": {"high": 0, "medium": 0, "low": 0},
                      "created": 0, "merged": 0, "unchanged": 0, "queued": 0, "backlogged": 0, "ledgered": 0,
                      "llm_classified": 0, "errors": [], "new_candidates": 0, "verified_ids": 0,
                      "retractions_found": 0, "maintained": [], "proposals": 0, "backfill_created": 0,
                      "revisit_pages": 0, "recovered_days": []}
        self.new_records = []  # (teknoloji id, yol, kayıt) — bilgi güncelleme değerlendirmesi için

    # ------------------------------------------------------------ yardımcılar
    def _tech_ok(self, nid):
        return self.counter["per_tech"].get(nid, 0) < self.cfg.max_per_tech

    def _count(self, source, nid):
        self.counter["archived"] += 1
        self.counter["by_source"][source] = self.counter["by_source"].get(source, 0) + 1
        self.counter["per_tech"][nid] = self.counter["per_tech"].get(nid, 0) + 1

    @staticmethod
    def _seen_keys(rec):
        # yalnızca arXiv kimlikleri hatırlanır; OpenAlex yeniden taramaları created_date ile ayrıştırılır
        return [s for s in rec.get("source_ids") or [] if s.startswith("arxiv:")]

    def process(self, recs, source, created_since=None, use_seen=True):
        """Sayfadaki kayıtları birleştir, sınıflandır; yüksek güven → backlog, orta güven → inceleme kuyruğu."""
        fresh = []
        for r in R.dedupe_batch(recs):
            if use_seen and any(self.state.is_seen(k) for k in self._seen_keys(r)):
                self.stats["skipped_seen"] += 1
                continue
            if created_since and (r.get("oa_created") or "9999") < created_since:
                self.stats["skipped_known"] += 1  # ilk taramada zaten mevcuttu
                continue
            fresh.append(r)
        for r in fresh:
            c = self.clf.classify(r)
            self.stats["classified"][c["confidence"]] += 1
            if c["confidence"] in ("high", "medium"):  # teknoloji bağlamındaki çalışmalar
                self.discovery.observe(r, c)
            if self.archive.find(r):  # mevcut kayıtla birleştirme bütçe harcamaz
                st, _ = self.archive.upsert(r, c)
                self.stats[st] += 1
            elif c["confidence"] == "high":
                key = entry_key(r)
                if key:
                    self.mem[key] = r
                    if self.backlog.add(r, c, source):
                        self.stats["backlogged"] += 1
            elif c["confidence"] == "medium":
                if self.queue.find(r):
                    self.queue.add(r, c, "", self.cfg.today)  # tekrar: birleştir
                elif self.stats["queued"] < self.cfg.review_per_run:
                    if self.queue.add(r, c, "orta güven: kesin konum için inceleme gerekli", self.cfg.today):
                        self.stats["queued"] += 1
                else:
                    self.queue.to_ledger({"keys": sorted(R.keys(r)), "title": r.get("title"), "record": r,
                                          "suggested": c.get("primary"), "score": c.get("score"),
                                          "candidates": c.get("candidates"), "added": self.cfg.today.isoformat()},
                                         "queue_run_cap")
                    self.stats["ledgered"] += 1
            self.state.mark_seen(self._seen_keys(r))

    # ------------------------------------------------------------ kaynaklar
    def _pending_days(self, cp, lag):
        end = self.cfg.today - timedelta(days=lag)
        last = parse_date(cp.get("last_complete_day")) or (end - timedelta(days=1))
        start = max(last + timedelta(days=1), end - timedelta(days=self.cfg.max_catchup_days - 1))
        if start > last + timedelta(days=1):
            cp.setdefault("skipped_days", []).append(f"{(last + timedelta(days=1)).isoformat()}..{(start - timedelta(days=1)).isoformat()}")
        return list(daterange(start, end))

    def _arxiv_day(self, cp, day, use_seen=True):
        """Bir gönderim gününü sayfa sayfa işler; cp içinde kalınan sayfa saklanır."""
        start = cp.get("start", 0) if cp.get("day") == day.isoformat() else 0
        cp.update(day=day.isoformat(), start=start)
        q = arxiv.day_query(day)
        while True:
            recs, total = arxiv.fetch_page(self.http, q, start, self.cfg.arxiv_page_size)
            self.stats["fetched"] += len(recs)
            self.process(recs, "arxiv", use_seen=use_seen)
            start += self.cfg.arxiv_page_size
            cp["start"] = start
            self.state.save_all()
            if not recs or start >= min(total, self.cfg.arxiv_max_results):
                break
        cp.update(start=0, day=None)

    def _openalex_day(self, cp, day, stream, created_since=None, max_pages=None):
        max_pages = max_pages or (self.cfg.openalex_max_pages if stream == "journal"
                                  else max(1, self.cfg.openalex_max_pages // 4))
        page = cp.get("page", 1) if cp.get("day") == day.isoformat() else 1
        cp.update(day=day.isoformat(), page=page)
        while page <= max_pages:
            recs, meta = openalex.list_day(self.http, self.cfg, day, page, stream)
            self.stats["fetched"] += len(recs)
            if created_since:
                self.stats["revisit_pages"] += 1
            self.process(recs, "openalex", created_since=created_since, use_seen=False)
            page += 1
            cp["page"] = page
            self.state.save_all()
            if len(recs) < self.cfg.openalex_per_page:
                break
        if page > max_pages:
            cp.setdefault("truncated_days", {})[day.isoformat()] = max_pages
        cp.update(page=1, day=None)

    def collect_arxiv(self):
        cp = self.state.checkpoint("arxiv")
        first = cp.setdefault("first_pass", {})
        for day in self._pending_days(cp, self.cfg.arxiv_lag_days):
            self._arxiv_day(cp, day)
            cp["last_complete_day"] = day.isoformat()
            first[day.isoformat()] = self.cfg.today.isoformat()
            self.state.save_all()
        # Geç duyurulan gönderimler: aynı gün N gün sonra yeniden taranır (görülenler atlanır)
        rv = cp.setdefault("revisited", {})
        for lag in self.cfg.arxiv_revisit_lags:
            day = self.cfg.today - timedelta(days=lag)
            tag = f"{day.isoformat()}@{lag}"
            if tag in rv or day.isoformat() not in first:  # yalnızca ilk taraması yapılmış günler
                continue
            self._arxiv_day(cp.setdefault("revisit_cp", {}), day)
            rv[tag] = self.cfg.today.isoformat()
            self.state.save_all()
        self._prune_revisits(cp, max(self.cfg.arxiv_revisit_lags or [0]))

    def collect_openalex(self):
        for stream in OPENALEX_STREAMS:
            cp = self.state.checkpoint(f"openalex-{stream}")
            first = cp.setdefault("first_pass", {})
            for day in self._pending_days(cp, self.cfg.openalex_lag_days):
                self._openalex_day(cp, day, stream)
                cp["last_complete_day"] = day.isoformat()
                first[day.isoformat()] = self.cfg.today.isoformat()
                self.state.save_all()
            # Geç dizinlenen yayınlar: ilk taramadan sonra OpenAlex'e eklenenler (created_date) işlenir
            rv = cp.setdefault("revisited", {})
            for lag in self.cfg.openalex_revisit_lags:
                day = self.cfg.today - timedelta(days=lag)
                tag = f"{day.isoformat()}@{lag}"
                since = first.get(day.isoformat())
                if tag in rv or not since:
                    continue
                self._openalex_day(cp.setdefault("revisit_cp", {}), day, stream, created_since=since)
                rv[tag] = self.cfg.today.isoformat()
                self.state.save_all()
            self._prune_revisits(cp, max(self.cfg.openalex_revisit_lags or [0]))

    def _prune_revisits(self, cp, max_lag):
        cutoff = (self.cfg.today - timedelta(days=max_lag + 5)).isoformat()
        for k in ("first_pass", "truncated_days"):
            cp[k] = {d: v for d, v in (cp.get(k) or {}).items() if d >= cutoff}
        cp["revisited"] = {t: v for t, v in (cp.get("revisited") or {}).items() if t.split("@")[0] >= cutoff}

    # ------------------------------------------------------------ tek seferlik kurtarma
    def plan_recovery(self):
        """Backlog öncesi sürümde bütçeye takılıp atılan kayıtlar için ilgili günleri yeniden tarama planı.
        Çalışma günlüğünden (run-log) bütçe nedeniyle kayıt atlanan çalışmaların günleri çıkarılır."""
        rec = self.state.checkpoint("recovery")
        if rec.get("planned"):
            return
        import json
        import os
        jobs = []
        p = self.state.path("run-log.jsonl")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if (e.get("budget_skipped") or 0) > 0 and (e.get("fetched") or 0) > 0:
                    d = date.fromisoformat(e["date"])
                    jobs.append({"source": "arxiv", "day": (d - timedelta(days=self.cfg.arxiv_lag_days)).isoformat()})
                    for st in OPENALEX_STREAMS:
                        jobs.append({"source": "openalex", "stream": st,
                                     "day": (d - timedelta(days=self.cfg.openalex_lag_days)).isoformat()})
        uniq = []
        for j in jobs:
            if j not in uniq:
                uniq.append(j)
        rec.update(planned=True, jobs=uniq, planned_at=self.cfg.today.isoformat())
        self.state.save_all()

    def run_recovery(self):
        rec = self.state.checkpoint("recovery")
        while rec.get("jobs"):
            j = rec["jobs"][0]
            cp = rec.setdefault("cp", {})
            day = date.fromisoformat(j["day"])
            if j["source"] == "arxiv" and "arxiv" in self.sources:
                self._arxiv_day(cp, day, use_seen=False)
            elif j["source"] == "openalex" and "openalex" in self.sources:
                self._openalex_day(cp, day, j["stream"])
            else:
                break
            self.stats["recovered_days"].append(f"{j['source']}{('/' + j['stream']) if j.get('stream') else ''}:{j['day']}")
            rec["jobs"].pop(0)
            rec.setdefault("done", []).append(j)
            self.state.save_all()

    # ------------------------------------------------------------ backlog'dan arşivleme
    def drain_backlog(self):
        """Günlük bütçe kadar kaydı öncelik sırasıyla arşivler. Gerekirse tam metadata yeniden çekilir."""
        counts = {nid: len(n["research"]) for nid, n in self.tree.nodes.items()}
        budget = self.cfg.max_archive - self.counter["archived"]
        if budget <= 0 or not len(self.backlog):
            return
        picked, per = [], {}
        for e in self.backlog.ordered(counts):
            if len(picked) >= budget * 2:
                break
            n = per.get(e["primary"], 0) + self.counter["per_tech"].get(e["primary"], 0)
            if n >= self.cfg.max_per_tech:
                continue
            per[e["primary"]] = per.get(e["primary"], 0) + 1
            picked.append(e)
        need_ax = [e["ids"]["arxiv"] for e in picked if e["key"] not in self.mem and e["ids"].get("arxiv")]
        need_oa = [e["ids"]["openalex"] for e in picked if e["key"] not in self.mem and not e["ids"].get("arxiv")
                   and e["ids"].get("openalex")]
        fetched = {}
        try:
            for i in range(0, len(need_ax), 50):
                for r in arxiv.fetch_ids(self.http, need_ax[i:i + 50]):
                    fetched[entry_key(r)] = r
                    if r.get("arxiv"):
                        fetched["arxiv:" + r["arxiv"]] = r
            for i in range(0, len(need_oa), 50):
                for r in openalex.by_ids(self.http, self.cfg, need_oa[i:i + 50]):
                    fetched[entry_key(r)] = r
                    for s in r.get("source_ids") or []:
                        fetched[s] = r
        except SourceUnavailable as ex:
            self.stats["errors"].append(f"backlog yeniden çekme: {ex}")
        for e in picked:
            if self.counter["archived"] >= self.cfg.max_archive:
                break
            if not self._tech_ok(e["primary"]):
                continue
            rec = self.mem.get(e["key"]) or fetched.get(e["key"]) or \
                (fetched.get("arxiv:" + e["ids"]["arxiv"]) if e["ids"].get("arxiv") else None) or \
                (fetched.get("openalex:" + e["ids"]["openalex"]) if e["ids"].get("openalex") else None)
            if rec is None:
                continue  # kaynak bu çalışmada erişilemedi; backlog'da kalır
            c = self.clf.classify(rec)
            if c["confidence"] != "high":
                self.backlog.remove(e["key"])
                if c["confidence"] == "medium":
                    self.queue.add(rec, c, "backlog'dan: güven düştü (taksonomi değişmiş olabilir)", self.cfg.today)
                else:
                    self.ledger.write(e, "backlog_reclassified_low")
                continue
            st, path = self.archive.upsert(rec, c)
            self.stats[st] += 1
            self.backlog.remove(e["key"])
            if st == "created":
                self._count(e.get("source") or "backlog", c["primary"])
                self.new_records.append((c["primary"], path, rec))

    def enforce_limits(self):
        counts = {nid: len(n["research"]) for nid, n in self.tree.nodes.items()}
        self.stats["ledgered"] += self.backlog.enforce_limits(counts)
        self.stats["ledgered"] += self.queue.enforce_limits(self.cfg.today)

    def refresh_queue(self):
        """Kuyruktaki kayıtlar yeniden sınıflandırılır (taksonomi büyüdükçe bazıları kesinleşir)."""
        keep = []
        for it in self.queue.items:
            rec = it.get("record") or {}
            c = self.clf.classify(rec) if rec else None
            if c and c["confidence"] == "high":
                if self.archive.find(rec):
                    self.archive.upsert(rec, c)
                elif self.backlog.add(rec, c, "queue"):
                    self.stats["backlogged"] += 1
                continue
            keep.append(it)
        self.queue.items = keep

    # ------------------------------------------------------------ LLM ile kuyruk çözümü
    def resolve_queue_with_llm(self):
        if not (self.llm and self.llm.available and self.llm.trusted_for_classification):
            return
        keep = []
        for item in self.queue.items:
            rec = item.get("record") or {}
            try:
                res = self.clf.classify(rec)
                out = llm_classify(self.llm, self.clf, rec, res)
            except (BudgetExceeded, LLMUnavailable) as e:
                self.log(f"LLM: {e}")
                keep.append(item)
                keep.extend(self.queue.items[len(keep):])
                break
            except (LLMError, ValueError) as e:
                item["llm_error"] = str(e)
                keep.append(item)
                continue
            if out and out.get("primary") and out.get("confidence") == "high" and self._tech_ok(out["primary"]) \
                    and self.counter["archived"] < self.cfg.max_archive:
                st, _ = self.archive.upsert(rec, out)
                self.stats[st] += 1
                self.stats["llm_classified"] += 1
                if st == "created":
                    self._count("llm", out["primary"])
            else:
                item["llm_suggestion"] = out
                keep.append(item)
        self.queue.items = keep

    # ------------------------------------------------------------ kimlik doğrulama
    def verify_identifiers(self):
        todo = [r for r in self.tree.research
                if r["meta"].get("doi") and r["meta"].get("identifier_verified") in (False, None, "pending")]
        for r in todo[: self.cfg.verify_per_run]:
            m = r["meta"]
            path = f"{kb.ROOT}/{r['path']}"
            try:
                info = crossref.lookup(self.http, self.cfg, m["doi"])
                how = "crossref" if info else ("doi.org" if crossref.doi_registered(self.http, m["doi"]) else "not_found")
            except SourceUnavailable as e:
                self.stats["errors"].append(f"verify: {e}")
                break
            meta, body = kb.parse_frontmatter(kb.read(path))
            meta["identifier_verified"] = how
            if info:
                if info.get("peer_reviewed") is True and meta.get("peer_reviewed") is not True:
                    meta["peer_reviewed"] = True
                if info.get("publication") and not meta.get("publication"):
                    meta["publication"] = info["publication"]
                rv = meta.get("related_versions") or []
                for x in info.get("has_preprint", []):
                    v = {"relation": "preprint", "doi": x.lower(), "source": "crossref"}
                    if v not in rv:
                        rv.append(v)
                for x in info.get("is_preprint_of", []):
                    v = {"relation": "published_version", "doi": x.lower(), "source": "crossref"}
                    if v not in rv:
                        rv.append(v)
                meta["related_versions"] = rv
            if how == "not_found":
                self.queue.items.append({"keys": sorted(kb.research_keys(meta)), "title": meta.get("title"),
                                         "url": meta.get("url"), "reason": "DOI hiçbir kayıt kuruluşunda bulunamadı",
                                         "added": self.cfg.today.isoformat(), "suggested": meta.get("primary_technology"),
                                         "candidates": [], "path": r["path"]})
            kb.write(path, kb.dump_frontmatter(meta) + "\n" + body)
            r["meta"] = meta
            self.stats["verified_ids"] += 1

    # ------------------------------------------------------------ geri çekme / düzeltme denetimi
    def check_retractions(self):
        recs = [r for r in self.tree.research if r["meta"].get("doi")]
        recs.sort(key=lambda r: str(r["meta"].get("retraction_checked") or ""))
        for r in recs[: self.cfg.retraction_checks_per_run]:
            m = r["meta"]
            try:
                notices = crossref.notices_for(self.http, self.cfg, m["doi"])
            except SourceUnavailable as e:
                self.stats["errors"].append(f"retraction: {e}")
                break
            self.apply_notices(r, notices)

    def apply_notices(self, r, notices):
        from .archive import retraction_banner
        path = f"{kb.ROOT}/{r['path']}"
        meta, body = kb.parse_frontmatter(kb.read(path))
        meta["retraction_checked"] = self.cfg.today.isoformat()
        severe = [n for n in notices if n["type"] in crossref.SEVERE]
        if notices:
            meta["notices"] = notices
        if severe and meta.get("retraction_status") != "retracted":
            meta["retraction_status"] = "retracted"
            body = kb.replace_section(body, 1, retraction_banner("retracted", severe) + (kb.get_section(body, 1) or ""))
            self.stats["retractions_found"] += 1
            self.stats["proposals"] += len(M.retraction_proposals(self.cfg, self.tree, meta, severe))
        elif notices and meta.get("retraction_status") in (None, "none_reported", "unknown"):
            meta["retraction_status"] = "corrected"
        kb.write(path, kb.dump_frontmatter(meta) + "\n" + body)
        r["meta"] = meta

    # ------------------------------------------------------------ bilgi bakımı
    def maintain(self):
        if not (self.llm and self.llm.available):
            return
        for nid in M.priority_queue(self.tree, self.cfg.maintain_nodes_per_run):
            try:
                res = M.fill_node(self.cfg, self.tree, nid, self.llm, self.http, openalex)
            except (BudgetExceeded, LLMUnavailable) as e:
                self.log(f"bakım durdu: {e}")
                break
            except (LLMError, SourceUnavailable, ValueError) as e:
                self.stats["errors"].append(f"maintain {nid}: {e}")
                continue
            self.stats["maintained"].append(res)
        # yeni araştırmalar: içerikli düğümler için anlamlı katkı değerlendirmesi (yalnızca öneri üretir)
        for nid, path, rec in self.new_records:
            if not rec.get("abstract"):
                continue
            rmeta = kb.parse_frontmatter(kb.read(f"{kb.ROOT}/{path}"))[0]
            try:
                prop = M.assess_new_research(self.cfg, self.tree, nid, rmeta, rec["abstract"], self.llm)
            except (BudgetExceeded, LLMUnavailable) as e:
                self.log(f"güncelleme değerlendirmesi durdu: {e}")
                break
            except (LLMError, ValueError) as e:
                self.stats["errors"].append(f"assess {nid}: {e}")
                continue
            if prop:
                self.stats["proposals"] += 1

    # ------------------------------------------------------------ tarihsel tamamlama
    def backfill(self, tech_ids=None, per_tech=None):
        """Belirli teknolojilerin çok atıf alan önemli çalışmaları (adı başlıkta geçen dergi/konferans yayınları).
        Günlük bütçeden ayrı; sınıflandırıcı çalışmayı yüksek güvenle aynı teknolojiye (veya alt ağacına)
        yerleştirmezse arşivlenmez."""
        qpath = f"{self.cfg.state_dir}/backfill-queue.json"
        queue = load_json(qpath, [])
        if tech_ids:
            queue = [t for t in tech_ids if t not in queue] + queue
        done = []
        for nid in queue[: self.cfg.backfill_techs_per_run if not tech_ids else len(tech_ids)]:
            if nid not in self.tree.nodes:
                done.append(nid)
                continue
            title = self.tree.nodes[nid]["meta"]["title"]
            try:
                recs = openalex.search_top(self.http, self.cfg, title, (per_tech or self.cfg.backfill_per_tech) * 3,
                                           field="title")
            except SourceUnavailable as e:
                self.stats["errors"].append(f"backfill {nid}: {e}")
                break
            sub = set(kb.subtree(self.tree, nid))
            taken = 0
            for r in recs:
                if taken >= (per_tech or self.cfg.backfill_per_tech):
                    break
                c = self.clf.classify(r)
                if c["primary"] in sub and c["confidence"] == "high":
                    c = {**c, "method": "deterministic+backfill"}
                    st, _ = self.archive.upsert(r, c)
                    self.stats[st] += 1
                    if st == "created":
                        taken += 1
                        self.stats["backfill_created"] += 1
                        self.counter["backfill"] += 1
            done.append(nid)
        save_json(qpath, [t for t in queue if t not in done])

    # ------------------------------------------------------------ ana akış
    def step(self, name, fn):
        t0 = time.time()
        try:
            fn()
        except SourceUnavailable as e:
            self.stats["errors"].append(f"{name}: kaynak erişilemez: {e}")
        except Exception as e:  # bir adımın hatası diğerlerini durdurmaz; durum kaydedilir
            self.stats["errors"].append(f"{name}: {type(e).__name__}: {e}")
            self.log(traceback.format_exc())
        finally:
            self.state.save_all()
            self.log(f"[{name}] {time.time() - t0:.1f} sn")

    def daily(self, backfill=True, maintain=True):
        self.step("kurtarma-planı", self.plan_recovery)
        self.step("kurtarma", self.run_recovery)
        if "arxiv" in self.sources:
            self.step("arxiv", self.collect_arxiv)
        if "openalex" in self.sources:
            self.step("openalex", self.collect_openalex)
        self.step("kuyruk-yenile", self.refresh_queue)
        self.step("backlog-arşivleme", self.drain_backlog)
        self.step("llm-kuyruk", self.resolve_queue_with_llm)
        self.step("kimlik-doğrulama", self.verify_identifiers)
        self.step("geri-çekme", self.check_retractions)
        self.step("keşif", self.run_discovery)
        if backfill:
            self.step("tarihsel", self.backfill)
        if maintain:
            self.step("bakım", self.maintain)
        self.finish()
        return self.stats

    def run_discovery(self):
        def count(phrase):
            return openalex.count_phrase(self.http, self.cfg, phrase)
        created = self.discovery.update_candidates(self.http, count)
        self.stats["new_candidates"] = len(created)
        self.discovery.prune()
        self.discovery.save()

    def finish(self):
        self.enforce_limits()
        self.ledger.flush()
        self.backlog.save()
        self.state.prune_seen(self.cfg.seen_days)
        self.state.seen = {k: v for k, v in self.state.seen.items() if k.startswith("arxiv:")}
        self.queue.save(self.tree)
        self.discovery.save()
        self.state.save_all()
        kb.cmd_reindex()
        self.stats["http_calls"] = dict(self.http.calls)
        self.stats["llm"] = {"calls": self.counter["llm_calls"], "usd": self.counter["llm_usd"]}
        self.stats["backlog_size"] = len(self.backlog)
        self.stats["queue_size"] = len(self.queue.items)
        self.state.append_runlog({"date": self.cfg.today.isoformat(), **{k: v for k, v in self.stats.items()
                                                                          if k != "maintained"},
                                  "maintained": [m.get("node") for m in self.stats["maintained"]]})
