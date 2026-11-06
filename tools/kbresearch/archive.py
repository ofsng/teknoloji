"""Araştırma Markdown arşivi: tek kanonik dosya, mükerrer tespiti, sürüm birleştirme, inceleme kuyruğu."""
import os
from datetime import date

import kb

from . import records as R
from .state import load_json, save_json

ABSTRACT_NOT_COPIED = ("_Özet kaynakta mevcut; yeniden yayım lisansı doğrulanamadığından depoya kopyalanmadı. "
                       "Özet için kaynağa bakın: {url}_")
NO_ABSTRACT = "_Kaynakta özet bulunmuyor; kayıt yalnızca bibliyografik bilgi içerir._"


def provenance_lines(rec_meta, today):
    out = []
    if rec_meta.get("doi"):
        out.append(f"- DOI: https://doi.org/{rec_meta['doi']}")
    if rec_meta.get("arxiv"):
        out.append(f"- arXiv: https://arxiv.org/abs/{rec_meta['arxiv']}")
    for sid in rec_meta.get("source_ids") or []:
        if sid.startswith("openalex:"):
            out.append(f"- OpenAlex: https://openalex.org/{sid.split(':', 1)[1]}")
    if rec_meta.get("url") and not any(rec_meta["url"] in l for l in out):
        out.append(f"- URL: {rec_meta['url']}")
    for v in rec_meta.get("related_versions") or []:
        rel = {"preprint": "Ön baskı sürümü", "published_version": "Yayımlanmış sürüm"}.get(v.get("relation"), v.get("relation"))
        tgt = (f"https://doi.org/{v['doi']}" if v.get("doi") else
               f"https://arxiv.org/abs/{v['arxiv']}" if v.get("arxiv") else v.get("journal_ref", ""))
        out.append(f"- {rel}: {tgt}" + (f" ({v['journal_ref']})" if v.get("journal_ref") and v.get("doi") else ""))
    out.append(f"- Metadata kaynakları: {', '.join(rec_meta.get('source_ids') or [])} "
               f"(toplama: {rec_meta.get('collected_at') or today})")
    return "\n".join(out)


def abstract_section(rec):
    if R.abstract_allowed(rec):
        quoted = "\n".join("> " + line for line in rec["abstract"].splitlines() if line.strip())
        return f"{quoted}\n\n*Özet kaynağı: {', '.join(rec.get('source_ids') or [])} — lisans: {rec['abstract_license']}. " \
               f"Tam metin incelenmedi.*", "abstract_only"
    if rec.get("abstract"):
        return ABSTRACT_NOT_COPIED.format(url=rec.get("url") or "—"), "metadata_only"
    return NO_ABSTRACT, "metadata_only"


def retraction_banner(status, notices):
    if status != "retracted":
        return ""
    det = "; ".join(f"{n.get('type')} {n.get('notice_doi') or ''} {n.get('date') or ''}".strip() for n in notices or [])
    return f"> ⚠ **Bu yayın geri çekilmiştir.** {det}\n> Bulguları güvenilir kabul edilmemelidir.\n\n"


class Archive:
    def __init__(self, tree, today=None):
        self.tree = tree
        self.today = (today or date.today()).isoformat()
        self.index = {}
        for r in tree.research:
            for k in kb.research_keys(r["meta"]):
                self.index[k] = r["path"]

    def find(self, rec):
        for k in R.keys(rec):
            if k in self.index:
                return self.index[k]
        return None

    def _register(self, meta, path):
        for k in kb.research_keys(meta):
            self.index[k] = path

    def upsert(self, rec, cls):
        """('created'|'merged'|'unchanged', göreli yol)."""
        existing = self.find(rec)
        if existing:
            return self._merge_into(existing, rec)
        return "created", self._create(rec, cls)

    def _meta_from(self, rec, cls):
        status = "retracted" if rec.get("is_retracted") else "none_reported"
        meta = {"title": rec.get("title"), "authors": (rec.get("authors") or [])[:30],
                "year": R.year_of(rec), "published_date": rec.get("published_date"),
                "updated_date": rec.get("updated_date"), "doi": rec.get("doi"), "arxiv": rec.get("arxiv"),
                "url": rec.get("url"), "publication": rec.get("publication"),
                "publication_type": rec.get("publication_type"), "peer_reviewed": rec.get("peer_reviewed"),
                "primary_technology": cls["primary"], "related_technologies": cls.get("related") or [],
                "classification_confidence": cls["confidence"], "classification_method": cls.get("method"),
                "keywords": (rec.get("keywords") or [])[:12], "source_ids": rec.get("source_ids") or [],
                "cited_by_count": rec.get("cited_by_count"), "abstract_license": rec.get("abstract_license"),
                "retraction_status": status, "related_versions": rec.get("related_versions") or [],
                "identifier_verified": "arxiv" if (rec.get("arxiv") and not rec.get("doi")) else False,
                "collected_at": self.today, "last_checked_at": self.today, "content_verified": False}
        if len(rec.get("authors") or []) > 30:
            meta["authors_truncated"] = True
        meta = {"research_id": kb.research_id(meta), **meta}
        return meta

    def _create(self, rec, cls):
        meta = self._meta_from(rec, cls)
        abstract, status = abstract_section(rec)
        meta["content_status"] = status
        node = self.tree.nodes[cls["primary"]]
        rdir = os.path.join(kb.ROOT, node["dir"], kb.RESEARCH_DIR)
        os.makedirs(rdir, exist_ok=True)
        fname = kb.research_filename(meta)
        path = os.path.join(rdir, fname)
        n = 2
        while os.path.exists(path):
            path = os.path.join(rdir, fname[:-3] + f"-{n}.md")
            n += 1
        sections = {1: retraction_banner(meta["retraction_status"], []) + abstract,
                    9: provenance_lines(meta, self.today)}
        kb.write(path, kb.render_research(meta, sections))
        keep = os.path.join(rdir, ".gitkeep")
        if os.path.exists(keep):
            os.remove(keep)
        rel = os.path.relpath(path, kb.ROOT)
        self._register(meta, rel)
        r = {"path": rel, "meta": meta, "tech": cls["primary"]}
        self.tree.research.append(r)
        node["research"].append(r)
        return rel

    def _merge_into(self, rel, rec):
        path = os.path.join(kb.ROOT, rel)
        text = kb.read(path)
        meta, body = kb.parse_frontmatter(text)
        old, orig_body = dict(meta), body
        if rec.get("doi") and not meta.get("doi"):
            meta["doi"] = rec["doi"]
        if rec.get("arxiv") and not meta.get("arxiv"):
            meta["arxiv"] = rec["arxiv"]
        if rec.get("peer_reviewed") is True and meta.get("peer_reviewed") is not True:
            meta["peer_reviewed"] = True
            meta["publication"] = rec.get("publication") or meta.get("publication")
            meta["publication_type"] = rec.get("publication_type") or meta.get("publication_type")
            if meta.get("arxiv"):
                rv = meta.get("related_versions") or []
                if not any(v.get("arxiv") == meta["arxiv"] for v in rv):
                    rv.append({"relation": "preprint", "arxiv": meta["arxiv"], "source": "merge"})
                meta["related_versions"] = rv
        meta["source_ids"] = list(dict.fromkeys((meta.get("source_ids") or []) + (rec.get("source_ids") or [])))
        if rec.get("cited_by_count") is not None:
            meta["cited_by_count"] = max(meta.get("cited_by_count") or 0, rec["cited_by_count"])
        for v in rec.get("related_versions") or []:
            rv = meta.get("related_versions") or []
            if v not in rv:
                rv.append(v)
            meta["related_versions"] = rv
        if rec.get("is_retracted") and meta.get("retraction_status") != "retracted":
            meta["retraction_status"] = "retracted"
            body = kb.replace_section(body, 1, retraction_banner("retracted", []) + (kb.get_section(body, 1) or ""))
        if meta.get("content_status") == "metadata_only" and R.abstract_allowed(rec):
            abstract, status = abstract_section(rec)
            body = kb.replace_section(body, 1, abstract)
            meta["content_status"] = status
            meta["abstract_license"] = rec.get("abstract_license")
        if meta == old and body == orig_body:
            return "unchanged", rel
        meta["last_checked_at"] = self.today
        body = kb.replace_section(body, 9, provenance_lines(meta, self.today))
        kb.write(path, kb.dump_frontmatter(meta) + "\n" + body)
        self._register(meta, rel)
        return "merged", rel


class ReviewQueue:
    """Güveni yetersiz sınıflandırmalar. Sınırlı (varsayılan 150), tekrarları birleştirir, önceliğe göre sıralar.
    Taşan, süresi dolan ya da çalışma başı sınırı aşan kayıtlar silinmez; deftere (ledger) yazılır."""

    def __init__(self, review_dir, max_items, ledger=None, expire_days=30):
        self.dir = review_dir
        self.path = os.path.join(review_dir, "classification-queue.json")
        self.items = load_json(self.path, [])
        self.max = max_items
        self.ledger = ledger
        self.expire_days = expire_days

    @staticmethod
    def priority(it):
        rec = it.get("record") or {}
        import math
        return (it.get("score") or 0) + (1.0 if rec.get("peer_reviewed") else 0.0) + \
            0.5 * math.log1p(rec.get("cited_by_count") or 0) + 0.3 * min(it.get("seen", 1) - 1, 3)

    def find(self, rec):
        ks = R.keys(rec)
        for it in self.items:
            if set(it["keys"]) & ks:
                return it
        return None

    def has(self, rec):
        return self.find(rec) is not None

    def add(self, rec, cls, reason, today):
        """Yeni öğe eklendiyse True. Aynı çalışma zaten kuyruktaysa birleştirilir."""
        it = self.find(rec)
        if it:
            it["keys"] = sorted(set(it["keys"]) | R.keys(rec))
            it["seen"] = it.get("seen", 1) + 1
            if (cls.get("score") or 0) > (it.get("score") or 0):
                it.update(candidates=cls.get("candidates"), suggested=cls.get("primary"), score=cls.get("score"))
            old = it.get("record") or {}
            it["record"] = R.merge(old, rec) if old else rec
            return False
        self.items.append({"keys": sorted(R.keys(rec)), "title": rec.get("title"), "url": rec.get("url"),
                           "doi": rec.get("doi"), "arxiv": rec.get("arxiv"), "candidates": cls.get("candidates"),
                           "suggested": cls.get("primary"), "confidence": cls.get("confidence"),
                           "score": cls.get("score"), "reason": reason, "added": today.isoformat(), "seen": 1,
                           "record": rec})
        return True

    def to_ledger(self, it, reason):
        if self.ledger:
            from .backlog import compact_ids
            self.ledger.write({"key": it["keys"][0] if it["keys"] else None, "ids": compact_ids(it.get("record") or {}),
                               "title": (it.get("title") or "")[:160], "primary": it.get("suggested"),
                               "score": it.get("score"), "added": it.get("added"), "candidates": it.get("candidates")},
                              reason)

    def enforce_limits(self, today):
        from datetime import timedelta
        cutoff = (today - timedelta(days=self.expire_days)).isoformat()
        keep, moved = [], 0
        for it in self.items:
            if (it.get("added") or "9999") < cutoff and not it.get("pinned"):
                self.to_ledger(it, "queue_expired")
                moved += 1
            else:
                keep.append(it)
        keep.sort(key=lambda it: -self.priority(it))
        for it in keep[self.max:]:
            self.to_ledger(it, "queue_overflow")
            moved += 1
        self.items = keep[:self.max]
        return moved

    def pop(self, idx):
        return self.items.pop(idx)

    def save(self, tree):
        self.items.sort(key=lambda it: -self.priority(it))
        save_json(self.path, self.items)
        lines = ["# Sınıflandırma İnceleme Kuyruğu", "",
                 "> Otomatik üretilir. Öncelik sırasına göre (puan, hakemli yayın, atıf, tekrar görülme). Çözmek için: "
                 "`python3 tools/autokb.py queue resolve N --tech ID` veya `queue drop N`. "
                 f"Kuyruk en fazla {self.max} kayıt tutar; taşanlar ve {self.expire_days} günden eskiler silinmez, "
                 "`state/ledger/` defterine yazılır.", "", f"Bekleyen: **{len(self.items)}**", "",
                 "| # | Başlık | Önerilen | Adaylar | Görülme | Neden |", "|---|---|---|---|---|---|"]
        for i, it in enumerate(self.items):
            cands = ", ".join(f"`{c}` ({s})" for c, s in (it.get("candidates") or [])[:3])
            title = (it.get("title") or "").replace("|", "\\|")
            link = f"[{title}]({it['url']})" if it.get("url") else title
            lines.append(f"| {i} | {link} | `{it.get('suggested')}` | {cands} | {it.get('seen', 1)} | {it.get('reason')} |")
        os.makedirs(self.dir, exist_ok=True)
        kb.write(os.path.join(self.dir, "CLASSIFICATION-QUEUE.md"), "\n".join(lines) + "\n")
