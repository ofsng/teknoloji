"""Kalıcı durum: Git'e işlenen küçük JSON dosyaları (GitHub Actions runner diski geçicidir).

SQLite yerine JSON seçildi: dosyalar metin olduğundan Git farkları okunabilir, birleştirme
çakışmaları çözülebilir ve ikili dosya depoyu şişirmez. Her yazım atomiktir (tmp + rename).
"""
import json
import os
import time
from datetime import date, timedelta


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


class State:
    def __init__(self, state_dir, today):
        self.dir = state_dir
        self.today = today
        self.checkpoints = load_json(self.path("checkpoints.json"), {})
        self.seen = load_json(self.path("seen.json"), {})
        self.counters = load_json(self.path("counters.json"), {})

    def path(self, name):
        return os.path.join(self.dir, name)

    # -- kontrol noktaları
    def checkpoint(self, source):
        return self.checkpoints.setdefault(source, {})

    def save_checkpoints(self):
        save_json(self.path("checkpoints.json"), self.checkpoints)

    # -- görülen kayıtlar (yeniden işlemeyi önler; 60 gün sonra budanır)
    def is_seen(self, key):
        return key in self.seen

    def mark_seen(self, keys):
        for k in keys:
            self.seen[k] = self.today.isoformat()

    def prune_seen(self, days=60):
        cutoff = (self.today - timedelta(days=days)).isoformat()
        self.seen = {k: v for k, v in self.seen.items() if v >= cutoff}

    def save_seen(self):
        save_json(self.path("seen.json"), self.seen)

    # -- günlük sayaçlar (yarıda kalan çalışma aynı gün devam ederse bütçe aşılmaz)
    def day_counter(self):
        key = self.today.isoformat()
        for k in [k for k in self.counters if k < (self.today - timedelta(days=7)).isoformat()]:
            del self.counters[k]
        return self.counters.setdefault(key, {"archived": 0, "per_tech": {}, "by_source": {}, "backfill": 0,
                                              "llm_calls": 0, "llm_usd": 0.0})

    def save_counters(self):
        save_json(self.path("counters.json"), self.counters)

    def save_all(self):
        self.save_checkpoints()
        self.save_seen()
        self.save_counters()

    def append_runlog(self, entry, keep=400):
        p = self.path("run-log.jsonl")
        lines = []
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                lines = f.read().splitlines()
        lines.append(json.dumps(entry, ensure_ascii=False, sort_keys=True))
        os.makedirs(self.dir, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines[-keep:]) + "\n")


class RunLock:
    """Aynı anda iki çalışmayı önler. Kilit Git'e işlenmez (.gitignore). 6 saatten eski kilit bayat sayılır."""

    def __init__(self, state_dir):
        self.p = os.path.join(state_dir, ".lock")

    def __enter__(self):
        os.makedirs(os.path.dirname(self.p), exist_ok=True)
        if os.path.exists(self.p) and time.time() - os.path.getmtime(self.p) < 6 * 3600:
            raise RuntimeError(f"Başka bir çalışma sürüyor (kilit: {self.p})")
        with open(self.p, "w") as f:
            f.write(str(os.getpid()))
        return self

    def __exit__(self, *exc):
        try:
            os.remove(self.p)
        except FileNotFoundError:
            pass


def daterange(start, end):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def parse_date(s):
    return date.fromisoformat(s) if s else None
