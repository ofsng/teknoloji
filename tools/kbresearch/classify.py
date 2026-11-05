"""Research Classifier: araştırmaları mevcut taksonomideki kalıcı teknoloji kimliklerine eşler.

Deterministik yöntem (önce, ücretsiz):
  1. Taksonominin İngilizce adları ve takma adlarından bir ifade dizini kurulur.
  2. Başlık, anahtar sözcükler, kaynak konu etiketleri ve özetteki ifade eşleşmeleri ağırlıklandırılır.
  3. Kaynağın kendi sınıflandırması (arXiv kategorisi, OpenAlex alanı) öncül (prior) olarak kullanılır.
  4. Üst düğümlerin eşleşmesi alt düğümü destekler; birden fazla kardeş eşit güçteyse çalışma üst
     düğümde tutulur (genel aileyi ele alan çalışma yanlışlıkla en derin klasöre itilmez).
  5. Güven: high → arşiv, medium → inceleme kuyruğu (veya LLM), low → arşive alınmaz.
"""
import re
from collections import defaultdict

import kb

FIELD_W = {"title": 3.0, "keywords": 1.5, "topics": 1.0, "abstract": 1.0}
HIGH, MEDIUM = 6.0, 3.0
# Tek başına geçtiğinde başka anlamlara da gelebilen tek sözcüklü düğüm adları
AMBIGUOUS = {
    "transformer", "attention", "translation", "transcription", "pruning", "quantization", "calibration",
    "clustering", "rolling", "casting", "fatigue", "creep", "tunneling", "bearing", "spring", "pump", "drilling",
    "welding", "forging", "extrusion", "oscillator", "amplifier", "inverter", "rectifier", "antenna", "laser",
    "diode", "catalysis", "metabolism", "ecology", "grasping", "teleoperation", "convection", "conduction",
    "equalization", "beamforming", "synchronization", "modulation", "interpolation", "regression", "optimization",
    "control", "compression", "rendering", "scheduling", "planning", "localization", "segmentation", "detection",
    "classification", "tracking", "simulation", "verification", "testing", "refactoring", "virtualization",
    "photochemistry", "epitaxy", "etching", "doping", "lithography", "bioprinting", "endoscopy", "electrosurgery",
    "silicon", "glass", "steel", "concrete", "cement", "hydrogel", "elastomer", "colloid", "polymer", "ceramic",
    "superconductivity", "magnetism", "acoustic", "optic", "holography", "spintronic", "phononic", "plasmonic",
    "consensus", "sharding", "hashing", "ethernet", "bluetooth", "dentistry", "oncology", "cardiology",
    "neurology", "radiology", "ophthalmology", "anesthesiology", "toxicology", "pharmacology", "immunology",
    "virology", "microbiology", "zoology", "physiology", "combustion", "turbulence", "rheology", "lubrication",
    "ergonomic", "packaging", "composting", "desalination", "biochar", "forestry", "silviculture", "aquaculture",
    "hydrology", "geology", "seismology", "geodesy", "oceanography", "meteorology", "cosmology", "astrobiology",
    "biomechanic", "biomimetic", "biophysic", "biosensor", "nanomedicine", "telemedicine", "micromobility",
    "maglev", "hyperloop", "tokamak", "stellarator", "triboelectric", "metamaterial", "metasurface", "metalens",
    "raft", "paxos", "tcp", "udp", "quic", "http", "rfid", "wi-fi", "analysis", "distillation", "statistic",
    "algebra", "geometry", "topology", "logic", "probability", "optic", "dentistry", "biochemistry", "endoscopy",
}
FIELD_MAP = {
    "Computer Science": ["computer-science", "human-computer-interaction", "data-storage-and-memory"],
    "Mathematics": ["mathematics"],
    "Decision Sciences": ["mathematics"],
    "Physics and Astronomy": ["physics", "photonics", "quantum-science-and-technology"],
    "Chemistry": ["chemistry"], "Chemical Engineering": ["chemistry"],
    "Materials Science": ["materials-science", "nanotechnology"],
    "Engineering": ["electrical-and-electronic-engineering", "mechanical-engineering", "civil-engineering",
                    "aerospace", "transportation", "manufacturing", "mechatronics-and-control", "robotics",
                    "measurement-and-sensor-technologies", "telecommunications", "imaging-and-visualization",
                    "photonics"],
    "Energy": ["energy-technologies", "nuclear-technologies"],
    "Environmental Science": ["environmental-and-climate-technologies", "earth-sciences"],
    "Earth and Planetary Sciences": ["earth-sciences", "physics", "mining-and-petroleum"],
    "Agricultural and Biological Sciences": ["agriculture-and-food", "biology-and-biotechnology"],
    "Biochemistry, Genetics and Molecular Biology": ["biology-and-biotechnology"],
    "Immunology and Microbiology": ["biology-and-biotechnology", "medicine-and-biomedical"],
    "Neuroscience": ["neuroscience"], "Psychology": ["neuroscience"],
    "Medicine": ["medicine-and-biomedical"], "Nursing": ["medicine-and-biomedical"],
    "Pharmacology, Toxicology and Pharmaceutics": ["medicine-and-biomedical"],
    "Health Professions": ["medicine-and-biomedical"], "Dentistry": ["medicine-and-biomedical"],
    "Veterinary": ["agriculture-and-food"],
}
ARXIV_ARCHIVE_MAP = {
    "cs": ["computer-science"], "math": ["mathematics"], "stat": ["statistics"],
    "eess": ["electrical-and-electronic-engineering", "telecommunications"], "q-bio": ["biology-and-biotechnology"],
    "quant-ph": ["quantum-science-and-technology", "quantum-mechanics"], "cond-mat": ["physics", "materials-science"],
    "astro-ph": ["astronomy-and-astrophysics"], "physics": ["physics"], "gr-qc": ["physics"], "hep-ex": ["physics"],
    "hep-ph": ["physics"], "hep-th": ["physics"], "hep-lat": ["physics"], "nucl-ex": ["physics"],
    "nucl-th": ["physics"], "nlin": ["dynamical-systems", "physics"], "math-ph": ["physics"],
}
TOKEN_RE = re.compile(r"[a-z0-9]+")
ACRO_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,6}s?\b")
URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+")


def stem(w):
    if len(w) <= 3:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith(("sses", "shes", "ches", "xes", "zes")):
        return w[:-2]
    if w.endswith(("ss", "us", "is")):
        return w
    if w.endswith("s"):
        return w[:-1]
    return w


def toks(text):
    return [stem(t) for t in TOKEN_RE.findall(kb.ascii_slug(text or "").lower().replace("-", " "))]


class Classifier:
    def __init__(self, tree):
        self.tree = tree
        self.first = defaultdict(list)   # ilk token -> [(token dizisi, node id, ifade ağırlığı, ifade)]
        self.acronyms = defaultdict(list)  # büyük harf kısaltma -> [node id]
        self.ref_index = defaultdict(set)  # "arXiv:cs.CR" -> {node id}
        for nid, n in tree.nodes.items():
            m = n["meta"]
            names = [m.get("title")] + list(m.get("aliases") or [])
            for i, name in enumerate(names):
                if not name:
                    continue
                name = re.sub(r"\(.*?\)", "", str(name)).strip()
                if ACRO_RE.fullmatch(name) and i > 0:
                    if len(name) >= 3:
                        self.acronyms[name].append(nid)
                    continue
                t = toks(name)
                if not t or (len(t) == 1 and len(t[0]) < 4):
                    continue
                if len(t) == 1 and i > 0:
                    continue  # tek sözcüklü sıradan takma adlar (ör. "Encoder", "Platforms") çok belirsiz
                if len(t) == 1:
                    w = 0.35 if (t[0] in AMBIGUOUS or n["depth"] <= 2) else 0.7
                else:
                    w = 1.0 + 0.6 * (len(t) - 1)
                if i > 0:
                    w *= 0.9  # takma ad, asıl addan biraz zayıf
                self.first[t[0]].append((tuple(t), nid, w, name))
            for ref in m.get("classification_refs") or []:
                self.ref_index[ref].add(nid)

    # -- öncüller (kaynağın kendi sınıflandırması)
    def priors(self, record):
        strong, weak = set(), set()
        cats = record.get("categories") or []
        for i, c in enumerate(cats):
            target = strong if i == 0 else weak
            if c.startswith("arXiv:"):
                code = c[6:]
                hits = self.ref_index.get(c) or set()
                archive = code.split(".")[0]
                hits = hits | self.ref_index.get(f"arXiv:{archive}", set())
                hits |= {x for x in ARXIV_ARCHIVE_MAP.get(archive, []) if x in self.tree.nodes}
                target |= hits
            elif c.startswith("OpenAlex-field:"):
                target |= {x for x in FIELD_MAP.get(c.split(":", 1)[1], []) if x in self.tree.nodes}
        return strong, weak - strong

    def _match(self, text, field, hits):
        text = URL_RE.sub(" ", text or "")
        t = toks(text)
        seen = defaultdict(int)
        for i, tok in enumerate(t):
            for seq, nid, w, name in self.first.get(tok, ()):
                if tuple(t[i:i + len(seq)]) == seq:
                    seen[(nid, name, w)] += 1
        for (nid, name, w), cnt in seen.items():
            occ = 1.0 + min(cnt - 1, 3) * 0.25
            hits[nid].append((field, name, FIELD_W[field] * w * occ))
        for acro in set(ACRO_RE.findall(text or "")):
            for nid in self.acronyms.get(acro, ()):
                hits[nid].append((field, acro, FIELD_W[field] * 0.6))

    def classify(self, record):
        hits = defaultdict(list)
        self._match(record.get("title"), "title", hits)
        self._match(" ; ".join(record.get("keywords") or []), "keywords", hits)
        self._match(" ; ".join(record.get("topics") or []), "topics", hits)
        self._match(record.get("abstract"), "abstract", hits)
        raw = {}
        for nid, hs in hits.items():
            per_name = defaultdict(float)
            for _, name, s in hs:
                per_name[name] += s
            vals = sorted(per_name.values(), reverse=True)
            raw[nid] = vals[0] + 0.3 * sum(vals[1:])
        strong, weak = self.priors(record)
        total = {}
        for nid, r in raw.items():
            anc = self.tree.ancestors(nid)
            chain = set(anc) | {nid}
            t = r + min(3.0, 0.4 * sum(raw.get(a, 0.0) for a in anc))
            if chain & strong:
                t += 1.5
            elif chain & weak:
                t += 0.75
            elif strong:
                t *= 0.75
            total[nid] = t
        if not total:
            return self._result(None, "low", 0.0, [], {}, hits)
        ranked = sorted(total.items(), key=lambda x: (-x[1], -self.tree.nodes[x[0]]["depth"]))
        best, best_s = ranked[0]
        # Kardeş kuralı: aynı üstün birden fazla alt teknolojisi benzer güçteyse üst düğümü seç
        parent = self.tree.nodes[best]["parent_id"]
        if parent not in (None, "root"):
            sibs = [s for n2, s in ranked[1:] if self.tree.nodes[n2]["parent_id"] == parent and s >= 0.8 * best_s]
            if sibs and parent in self.tree.nodes:
                best, best_s = parent, max(best_s, total.get(parent, 0.0) + best_s * 0.5)
        related_chain = set(self.tree.ancestors(best)) | {best}
        competitors = [(n2, s) for n2, s in ranked if n2 not in related_chain and best not in self.tree.ancestors(n2)]
        margin_ok = not competitors or competitors[0][1] <= 0.8 * best_s
        if best_s >= HIGH and margin_ok:
            conf = "high"
        elif best_s >= MEDIUM:
            conf = "medium"
        else:
            conf = "low"
        related = [n2 for n2, s in competitors if s >= 0.45 * best_s][:4]
        return self._result(best, conf, best_s, related, dict(ranked[:6]), hits)

    def _result(self, primary, conf, score, related, top, hits):
        ev = {nid: sorted({f"{f}:{name}" for f, name, _ in hits[nid]}) for nid in top}
        return {"primary": primary, "confidence": conf, "score": round(score, 2), "related": related,
                "candidates": [[k, round(v, 2)] for k, v in top.items()], "method": "deterministic", "evidence": ev}


# ---------------------------------------------------------------- LLM yardımı (isteğe bağlı)

LLM_SCHEMA = {
    "type": "object",
    "properties": {
        "technology_id": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "related_ids": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["technology_id", "confidence", "related_ids", "reason"],
    "additionalProperties": False,
}
LLM_SYSTEM = (
    "You classify scientific papers into a fixed technology taxonomy. You only see the title, abstract and "
    "source subject labels, never the full text. Choose the single most specific taxonomy node that the paper's "
    "main contribution is about; choose a more general node when the paper covers a whole family. If none of the "
    "candidates fits, answer technology_id \"none\". Use only ids from the candidate list. Confidence is high only "
    "when the abstract makes the main topic unambiguous.")


def candidate_pool(clf, result, extra=8):
    """LLM'e verilecek adaylar: deterministik adaylar + üstleri + üstlerin doğrudan alt düğümleri."""
    tree = clf.tree
    pool = []
    for nid, _ in result["candidates"]:
        for x in [nid] + tree.ancestors(nid)[:2]:
            if x not in pool:
                pool.append(x)
        for c in tree.nodes[nid]["children"][:extra]:
            if c not in pool:
                pool.append(c)
    return pool[:40]


def llm_classify(llm, clf, record, result):
    tree = clf.tree
    pool = candidate_pool(clf, result)
    if not pool:
        return None
    lines = [f"- {nid}: " + " > ".join(tree.nodes[a]["meta"].get("title", a) for a in reversed(tree.ancestors(nid)))
             + (" > " if tree.ancestors(nid) else "") + tree.nodes[nid]["meta"].get("title", nid) for nid in pool]
    user = (f"Candidates (id: path):\n" + "\n".join(lines) +
            f"\n\nTitle: {record.get('title')}\nSource subject labels: {', '.join(record.get('categories') or [])}; "
            f"{', '.join(record.get('topics') or [])}\nKeywords: {', '.join(record.get('keywords') or [])}\n"
            f"Abstract: {record.get('abstract') or '(no abstract available)'}")
    out = llm.json_call("classify", LLM_SYSTEM, user, LLM_SCHEMA, max_tokens=4000, effort="low")
    tid = out.get("technology_id")
    if tid not in tree.nodes or tid not in pool:
        return {"primary": None, "confidence": "low", "method": "llm", "reason": out.get("reason")}
    rel = [r for r in out.get("related_ids") or [] if r in tree.nodes and r != tid][:4]
    return {"primary": tid, "confidence": out.get("confidence"), "related": rel, "method": "llm",
            "reason": out.get("reason"), "score": result["score"], "candidates": result["candidates"]}
