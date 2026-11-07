"""Kalıcı bekleme kuyruğu (backlog) ve kayıt defteri (ledger): bütçeye takılan hiçbir araştırma kaybolmaz.

- Yüksek güvenli fakat günlük arşiv bütçesine sığmayan kayıtlar backlog'a girer; sonraki çalışmalar onları
  öncelik sırasıyla arşivler (önce hiç araştırması olmayan teknolojiler, sonra puan ve atıf).
- Backlog'da yalnızca kimlikler ve sınıflandırma tutulur (kayıt başına ~200 bayt); arşivlenirken tam metadata
  kaynaktan yeniden çekilir (arXiv id_list, OpenAlex openalex_id filtresi), böylece bilgi de güncellenmiş olur.
- Toplam ya da teknoloji başına sınırı aşan en düşük öncelikli kayıtlar silinmez, aylık defter dosyasına
  (state/ledger/YYYY-MM.jsonl.gz) yazılır; `autokb.py backlog restore` ile geri alınabilir.
"""
import gzip
import json
import math
import os

from . import records as R
from .state import load_json, save_json


def compact_ids(rec):
    ids = {}
    if rec.get("doi"):
        ids["doi"] = rec["doi"]
    if rec.get("arxiv"):
        ids["arxiv"] = rec["arxiv"]
    for s in rec.get("source_ids") or []:
        if s.startswith("openalex:"):
            ids["openalex"] = s.split(":", 1)[1]
    return ids


def entry_key(rec):
    ks = sorted(R.strong_keys(rec)) or sorted(R.keys(rec))
    return ks[0] if ks else None


class Ledger:
    def __init__(self, state_dir, today):
        self.dir = os.path.join(state_dir, "ledger")
        self.today = today
        self.buffer = []

    def write(self, entry, reason):
        self.buffer.append({**entry, "ledger_reason": reason, "ledger_date": self.today.isoformat()})

    def flush(self):
        if not self.buffer:
            return
        os.makedirs(self.dir, exist_ok=True)
        path = os.path.join(self.dir, f"{self.today.strftime('%Y-%m')}.jsonl.gz")
        with gzip.open(path, "at", encoding="utf-8") as f:
            for e in self.buffer:
                f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
        self.buffer = []

    def read_all(self):
        out = []
        if not os.path.isdir(self.dir):
            return out
        for fn in sorted(os.listdir(self.dir)):
            if fn.endswith(".jsonl.gz"):
                with gzip.open(os.path.join(self.dir, fn), "rt", encoding="utf-8") as f:
                    out += [json.loads(l) for l in f if l.strip()]
        return out


class Backlog:
    def __init__(self, cfg, ledger):
        self.cfg, self.ledger = cfg, ledger
        self.path = os.path.join(cfg.state_dir, "backlog.json")
        self.entries = load_json(self.path, {})

    def __len__(self):
        return len(self.entries)

    def add(self, rec, cls, source):
        key = entry_key(rec)
        if not key:
            return False
        e = self.entries.get(key)
        if e:
            e["ids"].update(compact_ids(rec))
            e["score"] = max(e["score"], cls["score"])
            e["seen"] = e.get("seen", 1) + 1
            return False
        self.entries[key] = {
            "key": key, "ids": compact_ids(rec), "title": (rec.get("title") or "")[:160],
            "primary": cls["primary"], "related": cls.get("related") or [], "score": cls["score"],
            "cited": rec.get("cited_by_count") or 0, "peer_reviewed": rec.get("peer_reviewed"),
            "published": rec.get("published_date"), "source": source, "added": self.cfg.today.isoformat(), "seen": 1}
        return True

    def priority(self, e, tech_counts):
        n = tech_counts.get(e["primary"], 0)
        coverage = 3.0 if n == 0 else (1.0 if n < 3 else 0.0)
        return coverage + e["score"] / 3.0 + 0.5 * math.log1p(e.get("cited") or 0) + \
            (0.5 if e.get("peer_reviewed") else 0.0)

    def ordered(self, tech_counts):
        return sorted(self.entries.values(), key=lambda e: (-self.priority(e, tech_counts), e["added"], e["key"]))

    def remove(self, key):
        return self.entries.pop(key, None)

    def enforce_limits(self, tech_counts):
        """Teknoloji başına ve toplam sınırı aşan en düşük öncelikli kayıtları deftere taşır."""
        moved = 0
        per = {}
        for e in self.ordered(tech_counts):
            per.setdefault(e["primary"], []).append(e)
        for tech, es in per.items():
            for e in es[self.cfg.backlog_per_tech:]:
                self.ledger.write(self.entries.pop(e["key"]), "backlog_per_tech_cap")
                moved += 1
        if len(self.entries) > self.cfg.backlog_max:
            for e in self.ordered(tech_counts)[self.cfg.backlog_max:]:
                self.ledger.write(self.entries.pop(e["key"]), "backlog_total_cap")
                moved += 1
        return moved

    def save(self):
        save_json(self.path, self.entries)

    def restore(self, keys=None, tech=None):
        """Defterden backlog'a geri al (ör. bütçe artırıldığında ya da bir teknoloji için)."""
        n = 0
        for e in self.ledger.read_all():
            if e.get("ledger_reason", "").startswith("backlog") and (keys is None or e["key"] in keys) and \
                    (tech is None or e["primary"] == tech) and e["key"] not in self.entries:
                self.entries[e["key"]] = {k: v for k, v in e.items() if not k.startswith("ledger_")}
                n += 1
        return n
