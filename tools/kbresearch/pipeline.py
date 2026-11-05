"""Günlük çalışma ve tarihsel tamamlama.

Her sayfa işlendikten sonra durum diske yazılır; çalışma kesilirse bir sonraki çalışma aynı gün/sayfadan
devam eder. Arşiv yazımı idempotenttir (mükerrer kayıt oluşmaz), bu yüzden aynı sayfanın yeniden
işlenmesi güvenlidir. Bir kaynak erişilemezse diğerleri çalışmaya devam eder.
"""
import math
import time
import traceback
from datetime import timedelta

import kb

from . import records as R
from .archive import Archive, ReviewQueue
from .classify import Classifier, llm_classify
from .discovery import Discovery
from .http import SourceUnavailable
from .llm import LLMUnavailable, BudgetExceeded, LLMError
from . import maintainer as M
from .sources import arxiv, crossref, openalex
from .state import State, daterange, parse_date, load_json, save_json


class Run:
    def __init__(self, cfg, http, llm=None, sources=("arxiv", "openalex"), log=print):
        self.cfg, self.http, self.log = cfg, http, log
        self.state = State(cfg.state_dir, cfg.today)
        self.counter = self.state.day_counter()
        self.tree = kb.Tree()
        self.clf = Classifier(self.tree)
        self.archive = Archive(self.tree, cfg.today)
        self.queue = ReviewQueue(cfg.review_dir, cfg.review_queue_max)
        self.discovery = Discovery(cfg, self.tree, self.clf)
        self.llm = llm
        self.sources = sources
        self.stats = {"fetched": 0, "skipped_seen": 0, "classified": {"high": 0, "medium": 0, "low": 0},
                      "created": 0, "merged": 0, "unchanged": 0, "queued": 0, "budget_skipped": 0,
                      "llm_classified": 0, "errors": [], "new_candidates": 0, "verified_ids": 0,
                      "retractions_found": 0, "maintained": [], "proposals": 0, "backfill_created": 0}
        self.new_records = []  # (araştırma meta, kayıt) — bilgi güncelleme değerlendirmesi için

    # ------------------------------------------------------------ yardımcılar
    def _budget_left(self, source):
        share = math.ceil(self.cfg.max_archive * self.cfg.source_share.get(source, 1.0))
        used = self.counter["by_source"].get(source, 0)
        return max(0, min(share - used, self.cfg.max_archive - self.counter["archived"]))

    def _tech_ok(self, nid):
        return self.counter["per_tech"].get(nid, 0) < self.cfg.max_per_tech

    def _count(self, source, nid):
        self.counter["archived"] += 1
        self.counter["by_source"][source] = self.counter["by_source"].get(source, 0) + 1
        self.counter["per_tech"][nid] = self.counter["per_tech"].get(nid, 0) + 1

    def _seen_keys(self, rec):
        return [s for s in rec.get("source_ids") or []]

    def process(self, recs, source, budget_per_page):
        """Sayfadaki kayıtları birleştir, sınıflandır, en iyileri arşivle, gerisini kuyruğa al."""
        fresh = []
        for r in R.dedupe_batch(recs):
            if any(self.state.is_seen(k) for k in self._seen_keys(r)):
                self.stats["skipped_seen"] += 1
                continue
            fresh.append(r)
        scored = []
        for r in fresh:
            c = self.clf.classify(r)
            self.stats["classified"][c["confidence"]] += 1
            if c["confidence"] in ("high", "medium"):  # teknoloji bağlamındaki çalışmalar
                self.discovery.observe(r, c)
            scored.append((r, c))
        # mevcut kayıtlarla eşleşenler her zaman birleştirilir (bütçe harcamaz)
        rest = []
        for r, c in scored:
            if self.archive.find(r):
                st, _ = self.archive.upsert(r, c)
                self.stats[st] += 1
            else:
                rest.append((r, c))
        high = sorted([x for x in rest if x[1]["confidence"] == "high"],
                      key=lambda x: (-x[1]["score"], -(x[0].get("cited_by_count") or 0)))
        taken = 0
        for r, c in high:
            if taken >= budget_per_page or self._budget_left(source) <= 0 or not self._tech_ok(c["primary"]):
                self.stats["budget_skipped"] += 1
                continue
            st, path = self.archive.upsert(r, c)
            self.stats[st] += 1
            if st == "created":
                taken += 1
                self._count(source, c["primary"])
                self.new_records.append((c["primary"], path, r))
        mediums = sorted([x for x in rest if x[1]["confidence"] == "medium"], key=lambda x: -x[1]["score"])
        for r, c in mediums:
            if self.stats["queued"] >= self.cfg.review_per_run:
                break
            if self.queue.add(r, c, "orta güven: kesin konum için inceleme gerekli", self.cfg.today):
                self.stats["queued"] += 1
        for r, _ in scored:
            self.state.mark_seen(self._seen_keys(r))

    # ------------------------------------------------------------ kaynaklar
    def _pending_days(self, cp, lag):
        end = self.cfg.today - timedelta(days=lag)
        last = parse_date(cp.get("last_complete_day")) or (end - timedelta(days=1))
        start = max(last + timedelta(days=1), end - timedelta(days=self.cfg.max_catchup_days - 1))
        if start > last + timedelta(days=1):
            cp.setdefault("skipped_days", []).append(f"{(last + timedelta(days=1)).isoformat()}..{(start - timedelta(days=1)).isoformat()}")
        return list(daterange(start, end))

    def collect_arxiv(self):
        cp = self.state.checkpoint("arxiv")
        for day in self._pending_days(cp, self.cfg.arxiv_lag_days):
            start = cp.get("start", 0) if cp.get("day") == day.isoformat() else 0
            cp.update(day=day.isoformat(), start=start)
            q = arxiv.day_query(day)
            while True:
                recs, total = arxiv.fetch_page(self.http, q, start, self.cfg.arxiv_page_size)
                self.stats["fetched"] += len(recs)
                pages = max(1, math.ceil(min(total, self.cfg.arxiv_max_results) / self.cfg.arxiv_page_size))
                self.process(recs, "arxiv", math.ceil(self._budget_left("arxiv") / pages) + 1)
                start += self.cfg.arxiv_page_size
                cp["start"] = start
                self.state.save_all()
                if not recs or start >= min(total, self.cfg.arxiv_max_results):
                    break
            cp.update(last_complete_day=day.isoformat(), start=0, day=None)
            self.state.save_all()

    def collect_openalex(self):
        for stream, max_pages in (("journal", self.cfg.openalex_max_pages),
                                  ("biorxiv-medrxiv", max(1, self.cfg.openalex_max_pages // 4))):
            cp = self.state.checkpoint(f"openalex-{stream}")
            for day in self._pending_days(cp, self.cfg.openalex_lag_days):
                page = cp.get("page", 1) if cp.get("day") == day.isoformat() else 1
                cp.update(day=day.isoformat(), page=page)
                while page <= max_pages:
                    recs, meta = openalex.list_day(self.http, self.cfg, day, page, stream)
                    self.stats["fetched"] += len(recs)
                    total_pages = min(max_pages, math.ceil((meta.get("count") or 0) / self.cfg.openalex_per_page) or 1)
                    self.process(recs, "openalex", math.ceil(self._budget_left("openalex") / total_pages) + 1)
                    page += 1
                    cp["page"] = page
                    self.state.save_all()
                    if len(recs) < self.cfg.openalex_per_page:
                        break
                cp.update(last_complete_day=day.isoformat(), page=1, day=None)
                self.state.save_all()

    # ------------------------------------------------------------ LLM ile kuyruk çözümü
    def resolve_queue_with_llm(self):
        if not (self.llm and self.llm.available):
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
        if "arxiv" in self.sources:
            self.step("arxiv", self.collect_arxiv)
        if "openalex" in self.sources:
            self.step("openalex", self.collect_openalex)
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
        self.state.prune_seen()
        self.queue.save(self.tree)
        self.discovery.save()
        self.state.save_all()
        kb.cmd_reindex()
        self.stats["http_calls"] = dict(self.http.calls)
        self.stats["llm"] = {"calls": self.counter["llm_calls"], "usd": self.counter["llm_usd"]}
        self.state.append_runlog({"date": self.cfg.today.isoformat(), **{k: v for k, v in self.stats.items()
                                                                          if k != "maintained"},
                                  "maintained": [m.get("node") for m in self.stats["maintained"]]})
