"""Technology Discovery: taksonomide olmayan teknik kavramları kanıt biriktirerek aday olarak önerir.

Kavram kaynakları (deterministik): metindeki kısaltma tanımları — "Graph Neural Networks (GNNs)" — ve
kaynağın anahtar sözcükleri. Bir ifade ancak birden çok bağımsız çalışmada (farklı ilk yazarlar, farklı aylar)
görülürse aday olur; tek makaledeki yeni bir ad aday olmaz. Adaylar insan onayı (verify) olmadan taksonomiye
eklenmez (KB_DISCOVERY_AUTO_VERIFY=1 ile yaprak düzeyinde otomatik onay açılabilir; varsayılan kapalı).
"""
import os
import re
from collections import Counter
from datetime import date, timedelta

import kb

from . import records as R
from .classify import toks
from .state import load_json, save_json

STOP = {"method", "approach", "framework", "model", "system", "study", "analysis", "result", "data", "new",
        "novel", "based", "using", "proposed", "case", "use", "effect", "role", "impact", "performance",
        "evaluation", "application", "review", "survey", "paper", "work", "task", "problem", "process",
        "technique", "strategy", "tool", "design", "development", "research", "experiment", "test", "set",
        "high", "low", "large", "small", "first", "two", "three", "multi", "single", "general", "specific",
        "patient", "cell", "level", "rate", "time", "group", "risk", "factor", "outcome", "association"}
# Teknoloji adları çoğunlukla bu baş isimlerle biter (hastalık, organizma, istatistik terimleri elenir)
TECH_HEADS = {"network", "model", "algorithm", "learning", "architecture", "protocol", "scheme", "code", "sensor",
              "device", "laser", "transistor", "battery", "reactor", "spectroscopy", "microscopy", "imaging",
              "printing", "synthesis", "method", "technique", "system", "framework", "encoder", "decoder",
              "transformer", "attention", "optimization", "optimizer", "estimation", "estimator", "filter", "codec",
              "coding", "modulation", "antenna", "array", "memory", "processor", "accelerator", "chip", "circuit",
              "material", "alloy", "composite", "coating", "membrane", "catalyst", "electrode", "electrolyte",
              "cell", "detector", "camera", "display", "lidar", "radar", "robot", "actuator", "gripper", "engine",
              "turbine", "propulsion", "thruster", "editing", "sequencing", "assay", "vaccine", "therapy", "probe",
              "platform", "pipeline", "language", "compiler", "database", "index", "graph", "agent", "policy",
              "planner", "controller", "control", "simulation", "solver", "sampling", "inference", "retrieval",
              "generation", "distillation", "quantization", "tokenizer", "embedding", "diffusion", "flow", "fusion",
              "lithography", "deposition", "etching", "qubit", "gate", "channel", "routing", "consensus",
              "signature", "encryption", "proof", "commitment", "hash", "ledger", "rollup"}
FUNCTION_WORDS = {"of", "and", "for", "the", "in", "a", "an", "with", "on", "to", "via", "based", "using"}
ACRO_DEF = re.compile(r"((?:[A-Za-z][\w'-]*[\s-]+){1,8}?)\(([A-Z][A-Za-z0-9-]{1,11})\)")


def initials(words):
    out = ""
    for w in words:
        for part in re.split(r"-", w):
            if part:
                out += part[0].lower()
    return out


def schwartz_hearst(long_form, acro):
    """Kısaltmanın uzun biçimini Schwartz & Hearst (2003) yöntemiyle bulur: kısaltma harfleri sondan başa
    uzun biçimde sırayla aranır, ilk harf bir sözcük başına denk gelmelidir."""
    s = re.sub(r"[^a-z0-9]", "", acro.lower())
    if acro.endswith("s") and acro[:-1].isupper():
        s = s[:-1]
    l = long_form.lower()
    si, li = len(s) - 1, len(l) - 1
    while si >= 0:
        c = s[si]
        while li >= 0 and (l[li] != c or (si == 0 and li > 0 and l[li - 1].isalnum())):
            li -= 1
        if li < 0:
            return None
        si -= 1
        li -= 1
    start = l.rfind(" ", 0, li + 1) + 1
    out = long_form[start:].strip()
    n = len(out.split())
    return out if 1 <= n <= min(len(s) + 5, 2 * len(s)) else None


def acronym_definitions(text):
    """Metindeki "Uzun Ad (KISALTMA)" tanımları -> [(uzun ad, kısaltma)]."""
    found = []
    for m in ACRO_DEF.finditer(text or ""):
        acro = m.group(2)
        if len(re.sub(r"[^A-Za-z]", "", acro)) < 2 or sum(c.isupper() for c in acro) < 2:
            continue
        lf = schwartz_hearst(m.group(1).strip(), acro)
        if lf and len(lf.split()) >= 2:
            found.append((lf, acro))
    return found


def term_key(phrase):
    return " ".join(toks(phrase))


def is_conceptual(key):
    t = key.split()
    return 2 <= len(t) <= 6 and t[-1] in TECH_HEADS and any(w not in STOP and not w.isdigit() for w in t[:-1])


class Discovery:
    def __init__(self, cfg, tree, clf):
        self.cfg, self.tree, self.clf = cfg, tree, clf
        self.terms_path = os.path.join(cfg.state_dir, "discovery-terms.json")
        self.cand_path = os.path.join(cfg.review_dir, "technology-candidates.json")
        self.terms = load_json(self.terms_path, {})
        self.cands = load_json(self.cand_path, {})
        self.known = {}       # ifade anahtarı -> node id
        self.known_acr = {}   # kısaltma (küçük harf) -> node id
        self.name_tokens = []  # (token kümesi, node id, ad) — çakışma kontrolü için
        for nid, n in tree.nodes.items():
            m = n["meta"]
            for name in [m.get("title")] + list(m.get("aliases") or []):
                if not name:
                    continue
                k = term_key(name)
                if k:
                    self.known.setdefault(k, nid)
                    content = {w for w in k.split() if w not in FUNCTION_WORDS}
                    if content:
                        self.name_tokens.append((content, nid, name))
                if re.fullmatch(r"[A-Z][A-Za-z0-9-]{1,11}", name) and sum(c.isupper() for c in name) >= 2:
                    self.known_acr.setdefault(name.lower().rstrip("s"), nid)
            words = [w for w in re.split(r"[\s-]+", m.get("title") or "") if w]
            if len(words) >= 3:  # kısa başlıkların baş harfleri rastlantısal eşleşme üretir
                self.known_acr.setdefault(initials(words), nid)

    # -- kanıt biriktirme
    def observe(self, rec, cls):
        today = self.cfg.today.isoformat()
        ks = sorted(R.strong_keys(rec) or R.keys(rec))
        if not ks:  # DOI, arXiv ve başlığı olmayan kayıt: kanıt olarak izlenemez
            return
        pid = ks[0]
        first_author = (rec.get("authors") or ["?"])[0]
        month = (rec.get("published_date") or today)[:7]
        # Kaynak: metinde tanımlanan kısaltmalar. Kaynak anahtar sözcükleri (ör. OpenAlex keywords) çoğunlukla
        # hastalık/organizma/istatistik terimleri olduğundan kullanılmaz.
        phrases = acronym_definitions(f"{rec.get('title') or ''}. {rec.get('abstract') or ''}")
        for phrase, acro in phrases:
            key = term_key(phrase)
            if not is_conceptual(key) or key in self.known:
                continue
            t = self.terms.setdefault(key, {"display": Counter(), "acronyms": [], "papers": [], "authors": [],
                                            "months": [], "sources": [], "techs": {}, "first_seen": today,
                                            "examples": []})
            if isinstance(t["display"], dict):
                t["display"] = Counter(t["display"])
            if pid in t["papers"]:
                continue
            t["display"][phrase] += 1
            if acro and acro not in t["acronyms"]:
                t["acronyms"].append(acro)
            t["papers"] = (t["papers"] + [pid])[-40:]
            if first_author not in t["authors"]:
                t["authors"] = (t["authors"] + [first_author])[-40:]
            if month not in t["months"]:
                t["months"].append(month)
            src = (rec.get("source_ids") or ["?"])[0].split(":")[0]
            if src not in t["sources"]:
                t["sources"].append(src)
            if cls and cls.get("primary"):
                t["techs"][cls["primary"]] = t["techs"].get(cls["primary"], 0) + 1
            if len(t["examples"]) < 6:
                t["examples"].append({"id": pid, "title": rec.get("title"), "url": rec.get("url"),
                                      "date": rec.get("published_date")})
            t["last_seen"] = today

    # -- aday üretimi
    def overlaps(self, key, limit=4):
        """Mevcut teknoloji adları/takma adlarıyla sözcük örtüşmesi (Jaccard): [(benzerlik, node id, ad)].
        Mevcut bir adın aday içinde tamamen geçmesi (ör. "large language model" ⊂ "multimodal large language
        model") çakışma değil alt tür işaretidir; variant_parent() ile ayrıca ele alınır."""
        cand = {w for w in key.split() if w not in FUNCTION_WORDS}
        out = {}
        for toks_, nid, name in self.name_tokens:
            inter = len(cand & toks_)
            if not inter:
                continue
            sim = round(inter / len(cand | toks_), 2)
            if sim > out.get(nid, (0,))[0]:
                out[nid] = (sim, nid, name)
        return sorted(out.values(), reverse=True)[:limit]

    def synonym_of(self, key, acronyms):
        """Kısaltma mevcut bir teknolojininkiyle aynı VE adlar anlamca örtüşüyorsa eş anlamlıdır. Yalnızca kısaltma
        aynıysa (ör. ANN = artificial neural network / approximate nearest neighbor) eş anlamlı sayılmaz."""
        for a in acronyms:
            hit = self.known_acr.get(a.lower().rstrip("s"))
            if hit and any(nid == hit and sim >= 0.34 for sim, nid, _ in self.overlaps(key, limit=50)):
                return hit
        return None

    def ambiguous_acronyms(self, key, acronyms):
        out = []
        for a in acronyms:
            hit = self.known_acr.get(a.lower().rstrip("s"))
            if hit and not self.synonym_of(key, [a]):
                out.append((a, hit))
        return out

    def assess_conflicts(self, c):
        """Aday kaydına çakışma bilgisini yazar; çok güçlü çakışmada adayı reddeder."""
        key = c["key"]
        ov = self.overlaps(key)
        c["overlaps"] = [{"technology_id": nid, "name": name, "similarity": sim} for sim, nid, name in ov]
        amb = self.ambiguous_acronyms(key, c.get("acronyms") or [])
        if amb:
            c["ambiguous_acronyms"] = [{"acronym": a, "existing": n} for a, n in amb]
        syn = self.synonym_of(key, c.get("acronyms") or [])
        if c["status"] == "rejected" and str(c.get("reason", "")).startswith("synonym_of:") and not syn:
            # eski sürümün yalnızca kısaltmaya dayalı ret kararları geri alınır
            c.update(status="candidate", reason=None, alias_proposal=False)
            c.setdefault("notes", []).append("Önceki eş anlamlı kararı yalnızca kısaltma eşleşmesine dayanıyordu; "
                                             "geri alındı (kısaltma belirsiz).")
        if c["status"] != "candidate":
            return
        if syn:
            c.update(status="rejected", reason=f"synonym_of:{syn}", alias_proposal=True)
        elif ov and ov[0][0] >= 0.8:
            c.update(status="rejected", reason=f"duplicate_of:{ov[0][1]}", alias_proposal=True)
        else:
            parent = self.variant_parent(key)
            # önerilen üst düğümle benzerlik beklenir (alt tür); başka düğümlerle benzerlik çakışma işaretidir
            others = [o for o in ov if o[1] not in (parent, c.get("parent_suggestion")) and o[0] >= 0.4]
            c["possible_duplicate"] = bool(others)
            if parent:
                c["variant_of"] = parent

    def variant_parent(self, key):
        words = key.split()
        best = None
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                sub = " ".join(words[i:j])
                if sub != key and sub in self.known and (best is None or j - i > best[1]):
                    best = (self.known[sub], j - i)
        return best[0] if best else None

    def update_candidates(self, http=None, count_fn=None):
        cfg = self.cfg
        today = cfg.today.isoformat()
        created, lit_checks = [], 0
        for key, t in self.terms.items():
            disp = Counter(t["display"]).most_common(1)[0][0] if t["display"] else key
            n_p, n_a, n_m = len(t["papers"]), len(t["authors"]), len(t["months"])
            enough = n_p >= cfg.discovery_min_papers and n_a >= cfg.discovery_min_authors and \
                (n_m >= 2 or n_p >= 2 * cfg.discovery_min_papers)
            c = self.cands.get(key)
            if c is None and not enough:
                continue
            if c is None:
                syn = self.synonym_of(key, t["acronyms"])
                parent = self.variant_parent(key)
                reason = "variant_of_existing" if parent else "co_classification"
                if not parent and t["techs"]:
                    parent = max(t["techs"].items(), key=lambda x: x[1])[0]
                c = {"key": key, "display": disp, "status": "candidate", "created": today,
                     "parent_suggestion": parent, "parent_reason": reason, "acronyms": t["acronyms"],
                     "literature_count": None, "notes": []}
                if syn:
                    c.update(status="rejected", reason=f"synonym_of:{syn}", alias_proposal=True,
                             notes=[f"Mevcut teknolojinin ({syn}) eş anlamlısı; takma ad önerisi."])
                elif parent and parent in self.tree.nodes and self.tree.nodes[parent]["depth"] <= 1:
                    c["structural"] = True
                    c["notes"].append("Önerilen üst düğüm ana disiplin; yeni alt disiplin yapısal değişikliktir, "
                                      "insan incelemesi gerekir.")
                self.cands[key] = c
                created.append(key)
            c.update(display=disp, acronyms=t["acronyms"], updated=today,
                     evidence={"papers": n_p, "first_authors": n_a, "months": n_m, "sources": t["sources"],
                               "examples": t["examples"], "co_classified": t["techs"]})
            self.assess_conflicts(c)
            if c["status"] == "candidate" and c.get("literature_count") is None and count_fn and \
                    lit_checks < cfg.discovery_lit_checks:
                lit_checks += 1
                try:
                    c["literature_count"] = count_fn(disp)
                    c["literature_checked"] = today
                except Exception as e:  # kaynak erişilemezse sonraki çalışmada denenir
                    c["notes"].append(f"literatür sayımı başarısız: {e}")
            if c["status"] == "candidate" and c.get("literature_count") is not None and \
                    c["literature_count"] < cfg.discovery_min_literature:
                c["low_literature"] = True
        return created

    def prune(self, days=120):
        cutoff = (self.cfg.today - timedelta(days=days)).isoformat()
        self.terms = {k: v for k, v in self.terms.items()
                      if len(v["papers"]) > 1 or v.get("last_seen", "9999") >= cutoff or k in self.cands}

    def save(self):
        terms = {k: {**v, "display": dict(v["display"])} for k, v in self.terms.items()}
        save_json(self.terms_path, terms)
        save_json(self.cand_path, self.cands)
        self.render()

    def render(self):
        by = {"candidate": [], "verified": [], "rejected": []}
        for c in self.cands.values():
            by.setdefault(c["status"], []).append(c)
        lines = ["# Yeni Teknoloji Adayları", "",
                 "> Otomatik üretilir. Onay: `python3 tools/autokb.py candidates verify \"<anahtar>\" --parent ID "
                 "--title-tr \"Türkçe Ad\"`; ret: `candidates reject \"<anahtar>\" --reason \"...\"`.", "",
                 f"Bekleyen aday: **{len(by['candidate'])}** · Onaylanan: **{len(by['verified'])}** · "
                 f"Reddedilen: **{len(by['rejected'])}**", "",
                 "## Bekleyen adaylar", "", "| Anahtar | Ad | Önerilen üst | Kanıt (makale/yazar/ay) | Literatür | Not |",
                 "|---|---|---|---|---|---|"]
        for c in sorted(by["candidate"], key=lambda c: -(c.get("evidence") or {}).get("papers", 0)):
            ev = c.get("evidence") or {}
            notes = "; ".join(c.get("notes") or []) + (" ⚠ literatür az" if c.get("low_literature") else "")
            if c.get("overlaps"):
                notes += (" ⚠ olası çakışma: " if c.get("possible_duplicate") else " benzer: ") + ", ".join(
                    f"`{o['technology_id']}` ({o['similarity']})" for o in c["overlaps"][:3])
            if c.get("ambiguous_acronyms"):
                notes += " · belirsiz kısaltma: " + ", ".join(f"{a['acronym']}→`{a['existing']}`"
                                                             for a in c["ambiguous_acronyms"])
            lines.append(f"| `{c['key']}` | {c['display']} {('(' + ', '.join(c['acronyms']) + ')') if c.get('acronyms') else ''} | "
                         f"`{c.get('parent_suggestion')}` ({c.get('parent_reason')}) | {ev.get('papers')}/"
                         f"{ev.get('first_authors')}/{ev.get('months')} | {c.get('literature_count')} | {notes} |")
        lines += ["", "## Onaylananlar", ""] + [f"- `{c['key']}` → `{c.get('technology_id')}` ({c.get('verified_at')})"
                                                for c in by["verified"]]
        lines += ["", "## Reddedilenler", ""] + [f"- `{c['key']}` — {c.get('reason')}" for c in by["rejected"]]
        os.makedirs(self.cfg.review_dir, exist_ok=True)
        kb.write(os.path.join(self.cfg.review_dir, "TECHNOLOGY-CANDIDATES.md"), "\n".join(lines) + "\n")

    # -- insan kararları
    def verify(self, key, parent, title=None, title_tr=None, force=False):
        c = self.cands.get(key)
        if not c or c["status"] != "candidate":
            raise ValueError(f"Bekleyen aday yok: {key}")
        self.assess_conflicts(c)
        if c["status"] != "candidate":
            raise ValueError(f"Aday mevcut bir teknolojiyle çakışıyor: {c.get('reason')}")
        if c.get("possible_duplicate") and not force:
            raise ValueError("Olası çakışma: " + ", ".join(f"{o['technology_id']} ({o['similarity']})"
                                                           for o in c.get("overlaps", [])[:3]) +
                             " — yine de eklemek için --force")
        title = title or c["display"]
        path = kb.create_tech(self.tree, parent, title, title_tr or title, status="emerging", confidence="medium",
                              aliases=c.get("acronyms") or [],
                              extra_meta={"discovered": {"key": key, "papers": (c.get("evidence") or {}).get("papers"),
                                                         "literature_count": c.get("literature_count")}})
        meta, _ = kb.parse_frontmatter(kb.read(os.path.join(path, kb.INDEX)))
        nid = meta["id"]
        # kanıt olarak arşivde bulunan çalışmalara ilişki ekle (taşıma yapılmaz)
        linked = 0
        ex_ids = set(self.terms.get(key, {}).get("papers", []))
        for r in self.tree.research:
            if kb.research_keys(r["meta"]) & ex_ids:
                p = os.path.join(kb.ROOT, r["path"])
                m, body = kb.parse_frontmatter(kb.read(p))
                rel = m.get("related_technologies") or []
                if nid not in rel:
                    m["related_technologies"] = rel + [nid]
                    kb.write(p, kb.dump_frontmatter(m) + "\n" + body)
                    linked += 1
        c.update(status="verified", technology_id=nid, verified_at=self.cfg.today.isoformat(), linked_research=linked)
        return nid, path

    def reject(self, key, reason):
        c = self.cands.get(key)
        if not c:
            raise ValueError(f"Aday yok: {key}")
        c.update(status="rejected", reason=reason, rejected_at=self.cfg.today.isoformat())
