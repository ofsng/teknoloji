#!/usr/bin/env python3
"""Technology-Knowledge-Base bakım aracı (yalnızca Python standart kütüphanesi).

Kaynak gerçeklik: klasör ağacı ve her klasördeki `_index.md` ön bilgisi (frontmatter).
`tools/seed/*.tax` dosyaları ilk kurulumda kullanılan taksonomi tanımlarıdır; `build`
yalnızca eksik klasörleri/dosyaları oluşturur, mevcut içeriğin üzerine yazmaz.
Yalnızca `<!-- AUTO... -->` blokları yeniden üretilir.

Komutlar:
  build                 Seed dosyalarından eksik klasörleri ve _index.md dosyalarını oluştur, sonra reindex.
  reindex               AUTO bloklarını ve merkezi indeksleri yeniden üret.
  check                 Doğrulama: kırık bağlantı, mükerrer teknoloji/DOI/arXiv, hiyerarşi, yetim klasör.
  stats                 Sayım raporu.
  suggest "metin"       Yeni bir teknoloji için olası üst konumları öner.
  add-tech              Yeni teknoloji klasörü ekle.
  add-research          Bir teknolojiye araştırma kaydı ekle (mükerrer kontrolüyle).
  find ID               Bir teknoloji kimliğinin yolunu göster.
  migrate-layout        _index.md ve araştırma dosyalarını 2. sürüm bölüm düzenine taşı (elle yazılmış içerik korunur).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(ROOT, "tools", "seed")
INDEX = "_index.md"
RESEARCH_DIR = "Arastirmalar"
# Kök düzeyinde taksonomi olmayan klasörler
SKIP_DIRS = {"tools", "templates", "review", "state", "research-index", RESEARCH_DIR}
LAYOUT_VERSION = 2
REL_KEYS = [("related", "İlişkili (Related)"), ("depends_on", "Bağımlı olduğu (Depends on)"),
            ("applied_in", "Kullanıldığı alanlar (Applied in)")]

TR_MAP = str.maketrans({"ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I",
                        "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U",
                        "â": "a", "Â": "A", "î": "i", "û": "u"})


def set_root(path):
    """Testler ve başka kökte çalışmak için kök dizini değiştir."""
    global ROOT, SEED_DIR
    ROOT = os.path.abspath(path)
    SEED_DIR = os.path.join(ROOT, "tools", "seed")


def ascii_slug(text):
    t = text.translate(TR_MAP)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = t.replace("&", "ve").replace("+", "-")
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)


def make_id(text):
    return ascii_slug(text).lower()


def norm_title(text):
    return re.sub(r"[^a-z0-9]+", "", ascii_slug(text).lower())


# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[3:end].strip("\n").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if " #" in val and not val.startswith(("\"", "[")):
            val = val.split(" #", 1)[0].strip()
        if val.startswith("["):
            try:
                val = json.loads(val)
            except ValueError:
                val = [v.strip().strip("\"'") for v in val.strip("[]").split(",") if v.strip()]
        elif val.startswith("\""):
            try:
                val = json.loads(val)
            except ValueError:
                val = val.strip("\"")
        elif val in ("", "null", "~"):
            val = None
        elif val in ("true", "false"):
            val = val == "true"
        elif re.fullmatch(r"-?\d+", val):
            val = int(val)
        meta[key.strip()] = val
    body = text[end + 4:]
    return meta, body.lstrip("\n")


def dump_value(v):
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if re.fullmatch(r"[A-Za-z0-9_./-][A-Za-z0-9_.:/-]*", s) and s not in ("true", "false", "null") \
            and not re.fullmatch(r"-?\d+", s):
        return s
    return json.dumps(s, ensure_ascii=False)


def dump_frontmatter(meta):
    return "---\n" + "".join(f"{k}: {dump_value(v)}".rstrip() + "\n" for k, v in meta.items()) + "---\n"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------- named AUTO blocks

def block_markers(name):
    if name == "AUTO":  # ana blok; 1. sürümle geriye uyumlu işaretler
        return "<!-- AUTO:BEGIN (kb.py reindex üretir; bu bloğu elle düzenlemeyin) -->", "<!-- AUTO:END -->"
    return f"<!-- AUTO:{name}:BEGIN (otomatik; elle düzenlemeyin) -->", f"<!-- AUTO:{name}:END -->"


def block_re(name):
    if name == "AUTO":
        return re.compile(r"<!-- AUTO:BEGIN.*?-->.*?<!-- AUTO:END -->", re.S)
    return re.compile(rf"<!-- AUTO:{name}:BEGIN.*?-->.*?<!-- AUTO:{name}:END -->", re.S)


AUTO_RE = block_re("AUTO")


def empty_block(name):
    b, e = block_markers(name)
    return f"{b}\n{e}"


def set_block(text, name, content):
    """`name` bloğunun içeriğini değiştir; blok yoksa metnin sonuna ekle."""
    b, e = block_markers(name)
    new = f"{b}\n{content.strip()}\n{e}" if content.strip() else f"{b}\n{e}"
    rx = block_re(name)
    if rx.search(text):
        return rx.sub(lambda _: new, text, count=1)
    return text.rstrip() + "\n\n" + new + "\n"


# ---------------------------------------------------------------- section helpers

PLACEHOLDER = "_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._"
INDEX_SECTIONS = [  # (numara, başlık, otomatik blok)
    (1, "Tanım", None), (2, "Çalışma prensibi", None), (3, "Tarihçe", None),
    (4, "Temel kavramlar", None), (5, "Temel yöntemler", None),
    (6, "Alt teknolojiler", "AUTO"), (7, "İlişkili teknolojiler", "AUTO"),
    (8, "Kullanım alanları", None), (9, "Avantajlar", None), (10, "Sınırlılıklar", None),
    (11, "Açık problemler", None), (12, "Önemli araştırmalar", "RESEARCH"),
    (13, "Güncel gelişmeler", "RECENT"), (14, "Kaynaklar", None),
]
# Bilgi bakımcısının doldurabileceği (elle/kaynaklı) bölümler
CONTENT_SECTIONS = [n for n, _, b in INDEX_SECTIONS if b is None]
SECTION_TITLES = {n: t for n, t, _ in INDEX_SECTIONS}
HEADING_RE = re.compile(r"^## (\d+)\. (.+?)[ \t]*$", re.M)


def is_placeholder(content):
    c = content.strip()
    return not c or c == PLACEHOLDER or c.startswith("_Henüz doldurulmadı")


def split_sections(body):
    """Gövdeyi (önsöz, [(numara, başlık, içerik)]) olarak ayır. AUTO blokları içerikte kalır."""
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        return body, []
    pre = body[:matches[0].start()]
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((int(m.group(1)), m.group(2), body[m.end():end].strip("\n")))
    return pre, out


def section_text(content):
    """Bölümün elle/kaynaklı yazılmış kısmı: ilk AUTO işaretine kadar olan metin."""
    return content.split("<!-- AUTO")[0].strip()


def get_section(body, number):
    _, secs = split_sections(body)
    for n, _, c in secs:
        if n == number:
            return section_text(c)
    return None


def replace_section(text, number, content):
    """Bir bölümün yazılı kısmını değiştir; bölümdeki AUTO blokları ve sonrası olduğu gibi kalır."""
    m = None
    for mm in HEADING_RE.finditer(text):
        if int(mm.group(1)) == number:
            m = mm
            break
    if not m:
        raise KeyError(number)
    nxt = HEADING_RE.search(text, m.end())
    end = nxt.start() if nxt else len(text)
    auto = text.find("<!-- AUTO", m.end())
    if 0 <= auto < end:
        end = auto
    return text[:m.end()] + "\n\n" + content.strip() + "\n\n" + text[end:]


def strip_blocks(content):
    return re.sub(r"<!-- AUTO:(?:\w+:)?BEGIN.*?<!-- AUTO:(?:\w+:)?END -->", "", content, flags=re.S).strip()


def index_body(title_line, contents=None, extra=None):
    """2. sürüm _index.md gövdesi. contents: {numara: metin}."""
    contents = contents or {}
    out = [title_line, "", empty_block("NAV"), ""]
    for n, t, blk in INDEX_SECTIONS:
        if blk == "AUTO" and n == 7:
            continue  # 6 ve 7 tek AUTO bloğunda üretilir
        if blk == "AUTO":
            out += [empty_block("AUTO"), ""]
            continue
        out += [f"## {n}. {t}", ""]
        text = contents.get(n)
        out += [text.strip() if text and text.strip() else PLACEHOLDER, ""]
        if blk:
            out += [empty_block(blk), ""]
    if extra:
        out += ["## 15. Ek notlar", "", extra.strip(), ""]
    return "\n".join(out)


def title_line(meta):
    return f"# {meta['title_tr']}" + (f" ({meta['title']})" if meta.get("title") and meta["title"] != meta["title_tr"] else "")


def new_index_text(meta, definition=None):
    meta = dict(meta)
    meta.setdefault("layout", LAYOUT_VERSION)
    meta.setdefault("content_status", "scope_note" if definition else "empty")
    meta.setdefault("content_sources", [])
    contents = {}
    if definition:
        contents[1] = "**Kapsam notu** (sınıflandırma açıklaması; kaynaklı tanım değildir): " + definition
    return dump_frontmatter(meta) + "\n" + index_body(title_line(meta), contents)


# ---------------------------------------------------------------- research file format

RESEARCH_SECTIONS = [(1, "Araştırmanın özeti"), (2, "Ele aldığı problem"), (3, "Kullanılan yöntem"),
                     (4, "Temel bulgular"), (5, "Teknik katkıları"), (6, "Sınırlılıklar"),
                     (7, "İlişkili teknolojiler"), (8, "İlişkili araştırmalar"), (9, "Kaynaklar")]
RESEARCH_FIELDS = ["research_id", "title", "authors", "year", "published_date", "updated_date", "doi", "arxiv",
                   "url", "publication", "publication_type", "research_type", "peer_reviewed",
                   "primary_technology", "related_technologies", "classification_confidence",
                   "classification_method", "keywords", "source_ids", "cited_by_count", "content_status",
                   "abstract_license", "retraction_status", "related_versions", "collected_at",
                   "last_checked_at", "content_verified"]
NO_FULLTEXT = "_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._"


def research_tech(meta):
    return meta.get("primary_technology") or meta.get("technology_id")


def render_research(meta, sections=None):
    """Araştırma dosyası metni. meta alan sırası RESEARCH_FIELDS'e göre, bilinmeyenler sona."""
    sections = sections or {}
    ordered = {k: meta.get(k) for k in RESEARCH_FIELDS if k in meta}
    ordered.update({k: v for k, v in meta.items() if k not in ordered})
    out = [dump_frontmatter(ordered), f"# {meta.get('title') or ''}", ""]
    for n, t in RESEARCH_SECTIONS:
        out += [f"## {n}. {t}", ""]
        if n == 7:
            out += [empty_block("TECH"), ""]
            continue
        text = sections.get(n)
        out += [text.strip() if text and text.strip() else (PLACEHOLDER if n in (8, 9) else NO_FULLTEXT), ""]
    return "\n".join(out)


# ---------------------------------------------------------------- seed parsing

def parse_seed_line(raw, fname, lineno):
    parts = [p.strip() for p in raw.split("|")]
    if len(parts) < 2:
        parts.append(parts[0])
    en, tr = parts[0], parts[1] or parts[0]
    opts = {}
    if len(parts) > 2:
        rest = "|".join(parts[2:])
        if "def=" in rest:  # def= her zaman en sonda; içinde ';' bulunabilir
            rest, _, opts["def"] = rest.partition("def=")
            opts["def"] = opts["def"].strip()
        for kv in rest.split(";"):
            if not kv.strip():
                continue
            if "=" not in kv:
                raise SystemExit(f"{fname}:{lineno}: geçersiz seçenek '{kv}'")
            k, _, v = kv.partition("=")
            opts[k.strip()] = v.strip()
    return en, tr, opts


def load_seed():
    nodes = []
    for fname in sorted(os.listdir(SEED_DIR)):
        if not fname.endswith(".tax"):
            continue
        stack = []  # (indent, node)
        base = None  # "@under <id>": bu dosyadaki kök düğümler başka dosyadaki bir düğümün altına yerleşir
        for lineno, line in enumerate(read(os.path.join(SEED_DIR, fname)).splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("@under "):
                target = line.split()[1]
                base = next((n for n in nodes if n["id"] == target), None)
                if base is None:
                    raise SystemExit(f"{fname}:{lineno}: @under hedefi bulunamadı: {target}")
                stack = []
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent % 2:
                raise SystemExit(f"{fname}:{lineno}: girinti 2'nin katı olmalı")
            en, tr, opts = parse_seed_line(line.strip(), fname, lineno)
            while stack and stack[-1][0] >= indent:
                stack.pop()
            if indent and not stack:
                raise SystemExit(f"{fname}:{lineno}: üst düğüm yok")
            if stack and indent != stack[-1][0] + 2:
                raise SystemExit(f"{fname}:{lineno}: girinti bir seviyeden fazla atlıyor")
            parent = stack[-1][1] if stack else base
            node = {
                "id": opts.get("id") or make_id(en),
                "title": en, "title_tr": tr,
                "slug": opts.get("slug") or ascii_slug(tr),
                "parent": parent, "opts": opts, "src": f"{fname}:{lineno}", "children": [],
            }
            if parent:
                parent["children"].append(node)
            nodes.append(node)
            stack.append((indent, node))
    ids = defaultdict(list)
    for n in nodes:
        ids[n["id"]].append(n["src"])
    dups = {k: v for k, v in ids.items() if len(v) > 1}
    if dups:
        for k, v in dups.items():
            print(f"HATA mükerrer id '{k}': {', '.join(v)}", file=sys.stderr)
        raise SystemExit(1)
    sibling = defaultdict(list)
    for n in nodes:
        sibling[(id(n["parent"]), n["slug"].lower())].append(n["src"])
    for (_, slug), v in sibling.items():
        if len(v) > 1:
            raise SystemExit(f"HATA aynı üst altında aynı klasör adı '{slug}': {v}")
    return nodes


def seed_path(node):
    parts = []
    while node:
        parts.append(node["slug"])
        node = node["parent"]
    return os.path.join(ROOT, *reversed(parts))


def split_list(v):
    return [x.strip() for x in v.split(",") if x.strip()] if v else []


def node_type(depth):
    return {1: "discipline", 2: "subdiscipline"}.get(depth, "technology")


def cmd_build(args):
    nodes = load_seed()
    created_dirs = created_files = 0
    for n in nodes:
        path = seed_path(n)
        depth = len(os.path.relpath(path, ROOT).split(os.sep))
        if not os.path.isdir(path):
            os.makedirs(path)
            created_dirs += 1
        rdir = os.path.join(path, RESEARCH_DIR)
        os.makedirs(rdir, exist_ok=True)
        keep = os.path.join(rdir, ".gitkeep")
        if not os.listdir(rdir):
            write(keep, "")
        ipath = os.path.join(path, INDEX)
        if os.path.exists(ipath):
            continue
        o = n["opts"]
        meta = {
            "id": n["id"], "title": n["title"], "title_tr": n["title_tr"], "type": node_type(depth),
            "parent": n["parent"]["id"] if n["parent"] else "root",
            "status": o.get("status", "established"),
            "classification_confidence": o.get("conf", "high"),
            "aliases": split_list(o.get("alias", "")),
            "related": split_list(o.get("rel")), "depends_on": split_list(o.get("dep")),
            "applied_in": split_list(o.get("app")),
            "classification_refs": split_list(o.get("src")),
            "content_verified": False, "created": date.today().isoformat(),
        }
        write(ipath, new_index_text(meta, o.get("def")))
        created_files += 1
    print(f"build: {created_dirs} yeni klasör, {created_files} yeni _index.md")
    cmd_reindex(args)


# ---------------------------------------------------------------- tree scan

class Tree:
    def __init__(self, with_research=True):
        self.nodes = {}          # id -> node dict
        self.by_path = {}        # rel dir -> id
        self.orphans = []        # dirs without _index.md
        self.dup_ids = []
        self.research = []
        self.top = []
        self.with_research = with_research
        self.scan()

    def scan(self):
        for dirpath, dirnames, filenames in os.walk(ROOT):
            rel = os.path.relpath(dirpath, ROOT)
            dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")) and
                                 not (rel == "." and d in SKIP_DIRS) and d != RESEARCH_DIR)
            if rel == ".":
                continue
            if INDEX not in filenames:
                self.orphans.append(rel)
                continue
            meta, _ = parse_frontmatter(read(os.path.join(dirpath, INDEX)))
            nid = meta.get("id") or f"<idsiz:{rel}>"
            node = {"id": nid, "meta": meta, "dir": rel, "depth": len(rel.split(os.sep)),
                    "children": [], "research": [], "incoming": []}
            if nid in self.nodes:
                self.dup_ids.append((nid, self.nodes[nid]["dir"], rel))
                continue
            self.nodes[nid] = node
            self.by_path[rel] = nid
            rdir = os.path.join(dirpath, RESEARCH_DIR)
            if self.with_research and os.path.isdir(rdir):
                for f in sorted(os.listdir(rdir)):
                    if f.endswith(".md"):
                        p = os.path.join(rdir, f)
                        rmeta, _ = parse_frontmatter(read(p))
                        r = {"path": os.path.relpath(p, ROOT), "meta": rmeta, "tech": nid}
                        node["research"].append(r)
                        self.research.append(r)
        for nid, n in self.nodes.items():
            parent_dir = os.path.dirname(n["dir"])
            n["parent_id"] = self.by_path.get(parent_dir, "root" if not parent_dir else None)
            if n["parent_id"] and n["parent_id"] != "root":
                self.nodes[n["parent_id"]]["children"].append(nid)
            elif n["parent_id"] == "root":
                self.top.append(nid)
        for nid, n in self.nodes.items():
            for key, _ in REL_KEYS:
                for t in n["meta"].get(key) or []:
                    if t in self.nodes:
                        self.nodes[t]["incoming"].append((nid, key))
        sort_key = lambda i: norm_title(self.nodes[i]["meta"].get("title_tr", i))
        self.top.sort(key=sort_key)
        for n in self.nodes.values():
            n["children"].sort(key=sort_key)

    def name(self, nid):
        m = self.nodes[nid]["meta"]
        return m.get("title_tr") or m.get("title") or nid

    def link(self, from_dir, nid, label=None):
        target = os.path.join(self.nodes[nid]["dir"], INDEX)
        rel = os.path.relpath(target, from_dir).replace(os.sep, "/")
        return f"[{label or self.name(nid)}]({rel})"

    def top_of(self, nid):
        while self.nodes[nid]["parent_id"] not in ("root", None):
            nid = self.nodes[nid]["parent_id"]
        return nid

    def ancestors(self, nid):
        out = []
        cur = self.nodes[nid]["parent_id"]
        while cur not in ("root", None):
            out.append(cur)
            cur = self.nodes[cur]["parent_id"]
        return out

    def walk(self):
        for t in self.top:
            yield from subtree(self, t)


# ---------------------------------------------------------------- reindex

def research_year(m):
    if m.get("year"):
        return int(m["year"])
    pd = str(m.get("published_date") or "")
    return int(pd[:4]) if pd[:4].isdigit() else None


def research_line(r, from_dir):
    m = r["meta"]
    rel = os.path.relpath(r["path"], from_dir).replace(os.sep, "/")
    authors = m.get("authors") or []
    who = (authors[0].split()[-1] + (" vd." if len(authors) > 1 else "")) if authors else "?"
    bits = [f"{who} ({research_year(m) or 'tarihsiz'})"]
    if m.get("publication"):
        bits.append(f"*{m['publication']}*")
    if m.get("peer_reviewed") is True:
        bits.append("hakemli")
    elif m.get("peer_reviewed") is False:
        bits.append("ön baskı / hakemsiz")
    if m.get("cited_by_count"):
        bits.append(f"atıf: {m['cited_by_count']}")
    warn = "⚠ **GERİ ÇEKİLDİ** — " if m.get("retraction_status") == "retracted" else ""
    title = (m.get("title") or os.path.basename(r["path"])).replace("[", "(").replace("]", ")")
    return f"- {warn}[{title}]({rel}) — " + " · ".join(bits)


def nav_block(tree, nid):
    n = tree.nodes[nid]
    d = n["dir"]
    crumbs = [tree.link(d, a) for a in reversed(tree.ancestors(nid))]
    home = os.path.relpath("TECHNOLOGIES.md", d).replace(os.sep, "/")
    return f"**Konum:** [Kök]({home}) › " + " › ".join(crumbs + [f"**{tree.name(nid)}**"])


def main_block(tree, nid, layout):
    n = tree.nodes[nid]
    d = n["dir"]
    out = []
    if layout < 2:
        out += [nav_block(tree, nid), "", "## 3. Üst teknoloji", ""]
        out.append(f"- {tree.link(d, n['parent_id'])}" if n["parent_id"] not in ("root", None) else "- Ana disiplin")
        sub, rel = "## 4. Alt teknolojiler", "## 5. İlişkili teknolojiler"
    else:
        sub, rel = "## 6. Alt teknolojiler", "## 7. İlişkili teknolojiler"
    out += ["", sub, ""]
    out += [f"- {tree.link(d, c)}" for c in n["children"]] or ["- _Yaprak düğüm (alt sınıflandırma yok)._"]
    out += ["", rel, ""]
    if layout >= 2:
        out.append(f"- **Üst teknoloji:** {tree.link(d, n['parent_id'])}" if n["parent_id"] not in ("root", None)
                   else "- **Üst teknoloji:** — (ana disiplin)")
    any_rel = False
    for key, label in REL_KEYS:
        targets = n["meta"].get(key) or []
        if targets:
            any_rel = True
            items = [tree.link(d, t) if t in tree.nodes else f"`{t}` (bulunamadı)" for t in targets]
            out.append(f"- **{label}:** " + ", ".join(items))
    if n["incoming"]:
        any_rel = True
        seen = list(dict.fromkeys(src for src, _ in n["incoming"]))
        out.append("- **Bu teknolojiye bağlananlar:** " + ", ".join(tree.link(d, s) for s in seen))
    if not any_rel and layout < 2:
        out.append("- _Tanımlı ilişki yok._")
    if layout < 2:
        out += ["", f"**Araştırma kayıtları:** {len(n['research'])}"]
        out += [research_line(r, d) for r in n["research"]]
    return "\n".join(out)


def subtree_research(tree, nid):
    out = []
    for s in subtree(tree, nid):
        out.extend(tree.nodes[s]["research"])
    return out


def research_block(tree, nid, limit=8):
    n = tree.nodes[nid]
    own = n["research"]
    allr = subtree_research(tree, nid)
    lines = [f"Arşivdeki kayıtlar — bu düğüm: **{len(own)}**, alt teknolojiler dahil: **{len(allr)}**."]
    if own:
        lines.append("")
        key = lambda r: (-(r["meta"].get("cited_by_count") or 0), research_year(r["meta"]) or 9999)
        lines += [research_line(r, n["dir"]) for r in sorted(own, key=key)[:limit]]
        if len(own) > limit:
            lines.append(f"- … ve {len(own) - limit} kayıt daha: [{RESEARCH_DIR}/]({RESEARCH_DIR}/)")
    return "\n".join(lines)


def recent_block(tree, nid, limit=8, days=365):
    n = tree.nodes[nid]
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rec = [r for r in subtree_research(tree, nid) if str(r["meta"].get("published_date") or "") >= cutoff]
    if not rec:
        return f"_Son {days} günde arşive eklenmiş kayıt yok. Bu liste kanıt düzeyini göstermez; ön baskılar hakemli değildir._"
    rec.sort(key=lambda r: str(r["meta"].get("published_date")), reverse=True)
    lines = [f"Son {days} gündeki kayıtlar (alt teknolojiler dahil; yeni bulgular kesin sonuç değildir):", ""]
    lines += [research_line(r, n["dir"]) for r in rec[:limit]]
    return "\n".join(lines)


def tech_block_for_research(tree, r):
    m = r["meta"]
    d = os.path.dirname(r["path"])
    lines = []
    if r["tech"] in tree.nodes:
        lines.append(f"- **Kanonik konum:** {tree.link(d, r['tech'])}")
    rel = [t for t in (m.get("related_technologies") or [])]
    if rel:
        lines.append("- **İlişkili:** " + ", ".join(tree.link(d, t) if t in tree.nodes else f"`{t}` (bulunamadı)" for t in rel))
    return "\n".join(lines)


def cmd_reindex(args=None):
    tree = Tree()
    changed = 0
    for nid in tree.nodes:
        path = os.path.join(ROOT, tree.nodes[nid]["dir"], INDEX)
        text = read(path)
        layout = tree.nodes[nid]["meta"].get("layout") or 1
        new = set_block(text, "AUTO", main_block(tree, nid, layout))
        if layout >= 2:
            new = set_block(new, "NAV", nav_block(tree, nid))
            new = set_block(new, "RESEARCH", research_block(tree, nid))
            new = set_block(new, "RECENT", recent_block(tree, nid))
        if new != text:
            write(path, new)
            changed += 1
    for r in tree.research:
        p = os.path.join(ROOT, r["path"])
        text = read(p)
        if block_re("TECH").search(text):
            new = set_block(text, "TECH", tech_block_for_research(tree, r))
            if new != text:
                write(p, new)
    write_technologies(tree)
    write_research_index(tree)
    write_relationships(tree)
    write_stats(tree)
    update_taxonomy_table(tree)
    print(f"reindex: {len(tree.nodes)} teknoloji düğümü, {changed} _index.md güncellendi, {len(tree.research)} araştırma")
    return tree


GEN_NOTE = "> Bu dosya `python3 tools/kb.py reindex` tarafından otomatik üretilir. Elle düzenlemeyin.\n"


def write_technologies(tree):
    lines = ["# Teknoloji İndeksi", "", GEN_NOTE, "Ana disiplinler:", ""]
    for t in tree.top:
        count = sum(1 for _ in subtree(tree, t)) - 1
        lines.append(f"- [{tree.name(t)}](#{anchor(tree.name(t))}) — {count} alt düğüm")
    for t in tree.top:
        lines += ["", f"## {tree.name(t)}", ""]
        for nid in subtree(tree, t):
            n = tree.nodes[nid]
            m = n["meta"]
            indent = "  " * (n["depth"] - 1)
            extra = []
            if m.get("status") and m["status"] != "established":
                extra.append(m["status"])
            if m.get("classification_confidence") and m["classification_confidence"] != "high":
                extra.append(f"güven: {m['classification_confidence']}")
            if m.get("content_status") and m["content_status"] not in ("empty", "scope_note"):
                extra.append(f"içerik: {m['content_status']}")
            if n["research"]:
                extra.append(f"{len(n['research'])} araştırma")
            en = f" — *{m['title']}*" if m.get("title") and m["title"] != m.get("title_tr") else ""
            tag = f" `[{', '.join(extra)}]`" if extra else ""
            lines.append(f"{indent}- {tree.link('.', nid)}{en}{tag}")
    write(os.path.join(ROOT, "TECHNOLOGIES.md"), "\n".join(lines) + "\n")


def subtree(tree, nid):
    yield nid
    for c in tree.nodes[nid]["children"]:
        yield from subtree(tree, c)


def anchor(text):
    a = text.lower().strip()
    a = re.sub(r"[^\w\- ]", "", a, flags=re.U)
    return a.replace(" ", "-")


def research_row(tree, r, from_dir):
    m = r["meta"]
    title = (m.get("title") or os.path.basename(r["path"])).replace("|", "\\|")
    path = os.path.relpath(r["path"], from_dir).replace(os.sep, "/")
    rid = m.get("research_id") or research_id(m)
    pr = {True: "hakemli", False: "ön baskı"}.get(m.get("peer_reviewed"), "")
    warn = "⚠ geri çekildi " if m.get("retraction_status") == "retracted" else ""
    tech = tree.link(from_dir, r["tech"]) if r["tech"] in tree.nodes else r["tech"]
    return (f"| {m.get('published_date') or research_year(m) or ''} | {warn}[{title}]({path}) | `{rid}` | "
            f"{tech} | {pr} |")


def write_research_index(tree):
    idx_dir = os.path.join(ROOT, "research-index")
    by_year = defaultdict(list)
    for r in tree.research:
        by_year[research_year(r["meta"]) or 0].append(r)
    lines = ["# Araştırma İndeksi", "", GEN_NOTE, f"Toplam kayıt: **{len(tree.research)}**", ""]
    if not tree.research:
        lines.append("_Henüz araştırma kaydı yok. Eklemek için: `python3 tools/kb.py add-research --help` "
                     "veya `python3 tools/autokb.py daily`_")
    else:
        per_top = defaultdict(int)
        for r in tree.research:
            if r["tech"] in tree.nodes:
                per_top[tree.top_of(r["tech"])] += 1
        lines += ["## Disipline göre", "", "| Disiplin | Kayıt |", "|---|---|"]
        lines += [f"| {tree.link('.', t)} | {c} |" for t, c in sorted(per_top.items(), key=lambda x: -x[1])]
        lines += ["", "## Yıla göre", "", "| Yıl | Kayıt |", "|---|---|"]
        for y in sorted(by_year, reverse=True):
            label = str(y) if y else "tarihsiz"
            lines.append(f"| [{label}](research-index/{label}.md) | {len(by_year[y])} |")
        latest = sorted(tree.research, key=lambda r: str(r["meta"].get("collected_at") or r["meta"].get("added") or ""),
                        reverse=True)[:50]
        lines += ["", "## Son eklenen 50 kayıt", "", "| Tarih | Başlık | Kimlik | Teknoloji | Tür |", "|---|---|---|---|---|"]
        lines += [research_row(tree, r, ".") for r in latest]
    write(os.path.join(ROOT, "RESEARCH-INDEX.md"), "\n".join(lines) + "\n")
    os.makedirs(idx_dir, exist_ok=True)
    wanted = set()
    for y, rs in by_year.items():
        label = str(y) if y else "tarihsiz"
        wanted.add(f"{label}.md")
        rows = sorted(rs, key=lambda r: (str(r["meta"].get("published_date") or ""), r["path"]))
        body = [f"# Araştırmalar — {label}", "", GEN_NOTE, f"[← Araştırma indeksi](../RESEARCH-INDEX.md)", "",
                "| Tarih | Başlık | Kimlik | Teknoloji | Tür |", "|---|---|---|---|---|"]
        body += [research_row(tree, r, "research-index") for r in rows]
        write(os.path.join(idx_dir, f"{label}.md"), "\n".join(body) + "\n")
    for f in os.listdir(idx_dir):
        if f.endswith(".md") and f not in wanted:
            os.remove(os.path.join(idx_dir, f))


def write_relationships(tree):
    edges = []
    for nid in tree.walk():
        for key, label in REL_KEYS:
            for t in tree.nodes[nid]["meta"].get(key) or []:
                edges.append((nid, key, t))
    cross = [e for e in edges if e[2] in tree.nodes and tree.top_of(e[0]) != tree.top_of(e[2])]
    lines = ["# İlişkiler ve Çapraz Bağlantılar", "", GEN_NOTE,
             "Her teknolojinin tek bir kanonik klasörü vardır. Birden fazla disiplini ilgilendiren teknolojiler "
             "kanonik konumlarında tutulur; diğer alanlarla bağlantı `_index.md` ön bilgisindeki "
             "`related`, `depends_on`, `applied_in` alanlarıyla kurulur.", "",
             f"Toplam ilişki: **{len(edges)}** — disiplinler arası: **{len(cross)}**", "",
             "## Disiplinler arası ilişkiler", "",
             "| Kaynak | Disiplin | İlişki | Hedef | Disiplin |", "|---|---|---|---|---|"]
    labels = dict(REL_KEYS)
    for s, k, t in cross:
        lines.append(f"| {tree.link('.', s)} | {tree.name(tree.top_of(s))} | {labels[k]} | "
                     f"{tree.link('.', t)} | {tree.name(tree.top_of(t))} |")
    lines += ["", "## Disiplin içi ilişkiler", "", "| Kaynak | İlişki | Hedef |", "|---|---|---|"]
    for s, k, t in edges:
        if (s, k, t) not in cross:
            tgt = tree.link('.', t) if t in tree.nodes else f"`{t}` (bulunamadı)"
            lines.append(f"| {tree.link('.', s)} | {labels[k]} | {tgt} |")
    write(os.path.join(ROOT, "RELATIONSHIPS.md"), "\n".join(lines) + "\n")


def compute_stats(tree):
    dirs = 0
    md = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if dirpath != ROOT:
            dirs += 1
        md += sum(1 for f in filenames if f.endswith(".md"))
    depth = max((n["depth"] for n in tree.nodes.values()), default=0)
    depth_hist = defaultdict(int)
    for n in tree.nodes.values():
        depth_hist[n["depth"]] += 1
    content = defaultdict(int)
    for n in tree.nodes.values():
        content[n["meta"].get("content_status") or "empty"] += 1
    leaves = sum(1 for n in tree.nodes.values() if not n["children"])
    per_top = {t: sum(1 for _ in subtree(tree, t)) for t in tree.top}
    return {"disciplines": len(tree.top), "nodes": len(tree.nodes),
            "technologies": len(tree.nodes) - len(tree.top), "leaves": leaves,
            "dirs_total": dirs, "md_files": md, "max_depth": depth,
            "depth_hist": dict(sorted(depth_hist.items())), "research": len(tree.research),
            "relations": sum(len(n["meta"].get(k) or []) for n in tree.nodes.values() for k, _ in REL_KEYS),
            "content_status": dict(sorted(content.items())),
            "content_verified": sum(1 for n in tree.nodes.values() if n["meta"].get("content_verified") is True),
            "per_top": per_top}


def write_stats(tree):
    s = compute_stats(tree)
    lines = ["# İstatistikler", "", GEN_NOTE,
             f"- Ana disiplin: **{s['disciplines']}**",
             f"- Teknoloji / alt teknoloji düğümü (ana disiplinler hariç): **{s['technologies']}**",
             f"- Toplam taksonomi düğümü: **{s['nodes']}** (yaprak: {s['leaves']})",
             f"- Toplam klasör (Arastirmalar/ ve tools/ dahil): **{s['dirs_total']}**",
             f"- Markdown dosyası: **{s['md_files']}**",
             f"- Maksimum hiyerarşi derinliği: **{s['max_depth']}**",
             f"- Araştırma kaydı: **{s['research']}**",
             f"- Tanımlı ilişki: **{s['relations']}**",
             f"- İnsan tarafından doğrulanmış içerik (`content_verified: true`): **{s['content_verified']}**", "",
             "## İçerik durumu", "", "| content_status | Düğüm |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in s["content_status"].items()]
    lines += ["", "## Derinlik dağılımı", "", "| Seviye | Düğüm |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in s["depth_hist"].items()]
    lines += ["", "## Disiplin başına düğüm", "", "| Disiplin | Düğüm |", "|---|---|"]
    lines += [f"| {tree.link('.', t)} | {c} |" for t, c in s["per_top"].items()]
    write(os.path.join(ROOT, "STATS.md"), "\n".join(lines) + "\n")
    return s


def update_taxonomy_table(tree):
    path = os.path.join(ROOT, "TAXONOMY.md")
    if not os.path.exists(path):
        return
    text = read(path)
    if not AUTO_RE.search(text):
        return
    rows = ["", "| Ana disiplin | Klasör | Düğüm | Sınıflandırma referansları |", "|---|---|---|---|"]
    for t in tree.top:
        refs = ", ".join(tree.nodes[t]["meta"].get("classification_refs") or [])
        rows.append(f"| {tree.link('.', t)} | `{tree.nodes[t]['dir']}/` | {sum(1 for _ in subtree(tree, t))} | {refs} |")
    write(path, set_block(text, "AUTO", "\n".join(rows) + "\n"))


# ---------------------------------------------------------------- research ids

def norm_doi(doi):
    d = (doi or "").strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d)
    return d or None


def norm_arxiv(ax):
    a = (ax or "").strip()
    a = re.sub(r"^(arxiv:|https?://(export\.)?arxiv\.org/(abs|pdf)/)", "", a, flags=re.I)
    a = re.sub(r"\.pdf$", "", a)
    a = re.sub(r"v\d+$", "", a)
    return a.lower() or None


def kb_id(meta):
    authors = meta.get("authors") or []
    first = norm_title(authors[0].split()[-1]) if authors else "anon"
    key = f"{norm_title(meta.get('title') or '')}|{research_year(meta) or ''}|{first}"
    return f"kb:{research_year(meta) or 'nd'}-{first}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"


def research_id(meta):
    """Yeni kayıt için kalıcı kimlik: doi > arxiv > kb (başlık+yıl+ilk yazar özeti)."""
    doi = norm_doi(meta.get("doi"))
    if doi and not doi.startswith("10.48550/arxiv."):
        return f"doi:{doi}"
    ax = norm_arxiv(meta.get("arxiv")) or (doi[len("10.48550/arxiv."):] if doi else None)
    if ax:
        return f"arxiv:{ax}"
    return kb_id(meta)


def research_keys(meta):
    """Mükerrer tespitinde kullanılan tüm anahtarlar (kayıt sonradan DOI/arXiv kazansa da eşleşir)."""
    keys = set()
    doi = norm_doi(meta.get("doi"))
    if doi:
        keys.add("doi:" + doi)
        if doi.startswith("10.48550/arxiv."):
            keys.add("arxiv:" + doi[len("10.48550/arxiv."):])
    ax = norm_arxiv(meta.get("arxiv"))
    if ax:
        keys.add("arxiv:" + ax)
    if meta.get("research_id"):
        keys.add(str(meta["research_id"]).lower() if not str(meta["research_id"]).startswith("kb:") else meta["research_id"])
    t = norm_title(meta.get("title") or "")
    if t:
        keys.add(f"title:{t}|{research_year(meta) or ''}")
    return keys


# ---------------------------------------------------------------- check

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def cmd_check(args):
    tree = Tree()
    errors, warnings, infos = [], [], []
    for nid, a, b in tree.dup_ids:
        errors.append(f"Mükerrer teknoloji id '{nid}': {a} ve {b}")
    for o in tree.orphans:
        errors.append(f"Yetim klasör (_index.md yok): {o}")
    titles = defaultdict(list)
    for nid, n in tree.nodes.items():
        m = n["meta"]
        for key in ("title", "title_tr"):
            if m.get(key):
                titles[norm_title(m[key])].append(nid)
        expected_parent = n["parent_id"] or "?"
        if m.get("parent") != expected_parent:
            errors.append(f"{n['dir']}: frontmatter parent='{m.get('parent')}' fakat klasör üstü='{expected_parent}'")
        for req in ("id", "title", "title_tr", "type", "parent", "status", "classification_confidence"):
            if not m.get(req):
                errors.append(f"{n['dir']}: zorunlu alan eksik: {req}")
        if m.get("id") and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(m["id"])):
            errors.append(f"{n['dir']}: id biçimi geçersiz: {m['id']}")
        if m.get("content_verified") is True and m.get("content_status") not in ("human_verified",):
            errors.append(f"{n['dir']}: content_verified=true yalnızca insan doğrulamasıyla (content_status: human_verified)")
        if m.get("content_status") == "ai_quotes_sourced":
            warnings.append(f"{n['dir']}: eski durum adı ai_quotes_sourced (→ ai_draft_sourced + content_mode: quotes)")
        base = os.path.basename(n["dir"])
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", base):
            errors.append(f"{n['dir']}: klasör adı ASCII/tire standardına uymuyor")
        for key, _ in REL_KEYS:
            for t in m.get(key) or []:
                if t not in tree.nodes:
                    errors.append(f"{n['dir']}: {key} hedefi bulunamadı: {t}")
                elif t == nid:
                    errors.append(f"{n['dir']}: kendine {key} ilişkisi")
                elif key != "applied_in" and is_ancestor(tree, t, nid):
                    warnings.append(f"{n['dir']}: {key} hedefi '{t}' zaten bir üst düğüm (gereksiz ilişki)")
        if m.get("type") == "discipline" and not n["children"]:
            warnings.append(f"{n['dir']}: ana disiplin fakat alt düğümü yok")
        if m.get("type") == "subdiscipline" and not n["children"]:
            infos.append(f"{n['dir']}: yaprak alt disiplin")
        if len(n["children"]) == 1:
            infos.append(f"{n['dir']}: tek çocuklu düğüm (gerçek alt tür mü, gereksiz derinlik mi gözden geçirin)")
        if (m.get("layout") or 1) < LAYOUT_VERSION:
            infos.append(f"{n['dir']}: eski bölüm düzeni (migrate-layout)")
        if len(os.path.join("Technology-Knowledge-Base", n["dir"], INDEX)) > 240:
            warnings.append(f"{n['dir']}: yol 240 karakteri aşıyor (Windows uyumluluğu)")
    for k, ids in titles.items():
        uniq = sorted(set(ids))
        if len(uniq) > 1:
            errors.append(f"Olası mükerrer teknoloji (aynı ad '{k}'): " + ", ".join(tree.nodes[i]["dir"] for i in uniq))
    for nid, n in tree.nodes.items():
        for a in n["meta"].get("aliases") or []:
            for other in titles.get(norm_title(a), []):
                if other != nid and not is_ancestor(tree, other, nid) and not is_ancestor(tree, nid, other):
                    warnings.append(f"{n['dir']}: takma ad '{a}' başka bir teknolojinin adı: {tree.nodes[other]['dir']}")
    # araştırma kayıtları
    seen = defaultdict(list)
    for r in tree.research:
        m = r["meta"]
        for k in research_keys(m):
            seen[k].append(r["path"])
        doi, ax = norm_doi(m.get("doi")), norm_arxiv(m.get("arxiv"))
        valid_ids = {research_id(m), kb_id(m)} | ({"doi:" + doi} if doi else set()) | ({"arxiv:" + ax} if ax else set())
        if not m.get("research_id"):
            warnings.append(f"{r['path']}: research_id yok")
        elif m["research_id"] not in valid_ids:
            warnings.append(f"{r['path']}: research_id ({m['research_id']}) DOI/arXiv/başlık bilgisiyle uyuşmuyor")
        if research_tech(m) != r["tech"]:
            errors.append(f"{r['path']}: primary_technology='{research_tech(m)}' fakat klasör '{r['tech']}'")
        for t in m.get("related_technologies") or []:
            if t not in tree.nodes:
                errors.append(f"{r['path']}: related_technologies hedefi bulunamadı: {t}")
    for k, paths in seen.items():
        if len(set(paths)) > 1:
            errors.append(f"Mükerrer araştırma ({k}): " + ", ".join(sorted(set(paths))))
    # kırık bağlantılar
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            for target in LINK_RE.findall(read(p)):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                t = target.split("#")[0]
                if t and not os.path.exists(os.path.normpath(os.path.join(dirpath, t))):
                    errors.append(f"Kırık bağlantı: {os.path.relpath(p, ROOT)} -> {target}")
    s = compute_stats(tree)
    errors, warnings = list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))
    if getattr(args, "verbose", False):
        for i in infos:
            print("BİLGİ:", i)
    for w in warnings:
        print("UYARI:", w)
    for e in errors:
        print("HATA:", e)
    print(f"\ncheck: {s['nodes']} düğüm, {s['research']} araştırma, {len(errors)} hata, {len(warnings)} uyarı, "
          f"{len(infos)} bilgi notu" + ("" if getattr(args, "verbose", False) else " (görmek için --verbose)"))
    return 1 if errors else 0


def is_ancestor(tree, anc, nid):
    return anc in tree.ancestors(nid)


# ---------------------------------------------------------------- migrate

OLD_TO_NEW = {"1": 1, "2": 2, "6": 4, "7": 3, "9": 11, "10": 14}


def migrate_index(path):
    """1. sürüm _index.md → 2. sürüm. Elle yazılmış içerik eşlenen bölüme ya da 'Ek notlar'a taşınır."""
    text = read(path)
    meta, body = parse_frontmatter(text)
    if (meta.get("layout") or 1) >= LAYOUT_VERSION:
        return False
    _, secs = split_sections(strip_blocks(body))
    contents, extra = {}, []
    for n, title, content in secs:
        content = section_text(content)
        if is_placeholder(content) or n in (3, 4, 5):  # 3-5 eskiden otomatikti
            continue
        new_n = OLD_TO_NEW.get(str(n))
        if new_n:
            contents[new_n] = (contents.get(new_n, "") + "\n\n" + content).strip()
        else:
            extra.append(f"**{title}**\n\n{content}")
    scope = meta.get("type") == "discipline" and 1 in contents and "Kapsam notu" not in contents[1] \
        and meta.get("content_status") in (None, "empty", "scope_note")
    if scope:
        contents[1] = "**Kapsam notu** (sınıflandırma açıklaması; kaynaklı tanım değildir): " + contents[1]
    meta["layout"] = LAYOUT_VERSION
    meta.setdefault("content_status", "scope_note" if scope else ("empty" if not contents and not extra else "manual"))
    meta.setdefault("content_sources", [])
    write(path, dump_frontmatter(meta) + "\n" + index_body(title_line(meta), contents, "\n\n".join(extra) or None))
    return True


OLD_RESEARCH_TO_NEW = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 9}


def migrate_research(path):
    text = read(path)
    meta, body = parse_frontmatter(text)
    if block_re("TECH").search(body):
        return False
    _, secs = split_sections(body)
    sections = {}
    for n, title, content in secs:
        content = section_text(content)
        if not is_placeholder(content) and n in OLD_RESEARCH_TO_NEW:
            sections[OLD_RESEARCH_TO_NEW[n]] = content
    if "technology_id" in meta and "primary_technology" not in meta:
        meta["primary_technology"] = meta.pop("technology_id")
    if meta.get("year") and not meta.get("published_date"):
        meta["published_date"] = str(meta["year"])
    meta.setdefault("peer_reviewed", None)
    meta.setdefault("source_ids", ["manual"])
    meta.setdefault("content_status", "metadata_only")
    meta.setdefault("retraction_status", "unknown")
    meta.setdefault("classification_confidence", "high")
    meta.setdefault("classification_method", "manual")
    if meta.get("added") and not meta.get("collected_at"):
        meta["collected_at"] = meta.pop("added")
    write(path, render_research(meta, sections))
    return True


def cmd_migrate_layout(args):
    tree = Tree()
    ni = sum(migrate_index(os.path.join(ROOT, n["dir"], INDEX)) for n in tree.nodes.values())
    nr = sum(migrate_research(os.path.join(ROOT, r["path"])) for r in tree.research)
    print(f"migrate-layout: {ni} _index.md, {nr} araştırma dosyası taşındı")
    cmd_reindex()


# ---------------------------------------------------------------- other commands

def cmd_stats(args):
    s = compute_stats(Tree())
    for k, v in s.items():
        if k != "per_top":
            print(f"{k}: {v}")


def stem(w):
    # İngilizce çoğul eki ve yaygın Türkçe çoğul/iyelik ekleri için kaba kök bulma
    for suf in ("leri", "lari", "ler", "lar", "ies", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def tokens(text):
    return {stem(w) for w in re.split(r"[^a-z0-9]+", ascii_slug(text).lower()) if len(w) > 2}


def cmd_suggest(args):
    tree = Tree(with_research=False)
    q = tokens(args.text)
    if not q:
        raise SystemExit("Sorgu çok kısa")
    scored = []
    for nid, n in tree.nodes.items():
        m = n["meta"]
        own = tokens(" ".join([m.get("title", ""), m.get("title_tr", "")] + (m.get("aliases") or [])))
        path = tokens(n["dir"].replace(os.sep, " "))
        exact = any(q == tokens(t) for t in [m.get("title", ""), m.get("title_tr", "")] + (m.get("aliases") or []))
        score = 3 * len(q & own) + len(q & path) + 0.1 * n["depth"] - 0.5 * len(own - q) + (10 if exact else 0)
        if q & own or q & path:
            scored.append((score, nid, exact))
    scored.sort(reverse=True)
    if not scored:
        print("Eşleşme yok. Ana disiplinlerden birini seçin: " + ", ".join(tree.top))
        return
    print("Olası üst konumlar (en uygun önce). Aynı ad zaten varsa yeni klasör açmayın:\n")
    for score, nid, exact in scored[: args.limit]:
        print(f"  {score:5.1f}  {nid:45s} {tree.nodes[nid]['dir']}" + ("   <-- ZATEN MEVCUT" if exact else ""))


def create_tech(tree, parent, title, title_tr=None, nid=None, slug=None, status="established", confidence="medium",
                aliases=(), related=(), depends_on=(), applied_in=(), refs=(), extra_meta=None):
    """Yeni teknoloji klasörü oluştur ve yolunu döndür. Tekrarları reddeder."""
    if parent not in tree.nodes and parent != "root":
        raise ValueError(f"Üst teknoloji bulunamadı: {parent}")
    nid = nid or make_id(title)
    if nid in tree.nodes:
        raise ValueError(f"Bu id zaten var: {nid} -> {tree.nodes[nid]['dir']}")
    for other in tree.nodes.values():
        names = [other["meta"].get("title", ""), other["meta"].get("title_tr", "")] + (other["meta"].get("aliases") or [])
        if norm_title(title) in [norm_title(x) for x in names if x]:
            raise ValueError(f"Aynı adlı teknoloji zaten var: {other['dir']}")
    parent_dir = tree.nodes[parent]["dir"] if parent != "root" else ""
    path = os.path.join(ROOT, parent_dir, slug or ascii_slug(title_tr or title))
    if os.path.exists(path):
        raise ValueError(f"Klasör zaten var: {path}")
    depth = len(os.path.relpath(path, ROOT).split(os.sep))
    os.makedirs(os.path.join(path, RESEARCH_DIR))
    write(os.path.join(path, RESEARCH_DIR, ".gitkeep"), "")
    meta = {"id": nid, "title": title, "title_tr": title_tr or title, "type": node_type(depth),
            "parent": parent, "status": status, "classification_confidence": confidence,
            "aliases": list(aliases), "related": list(related), "depends_on": list(depends_on),
            "applied_in": list(applied_in), "classification_refs": list(refs), "content_verified": False,
            "created": date.today().isoformat()}
    meta.update(extra_meta or {})
    write(os.path.join(path, INDEX), new_index_text(meta))
    return path


def cmd_add_tech(args):
    tree = Tree(with_research=False)
    try:
        path = create_tech(tree, args.parent, args.title, args.title_tr, args.id, args.slug, args.status,
                           args.confidence, split_list(args.aliases), split_list(args.related),
                           split_list(args.depends_on), split_list(args.applied_in), split_list(args.refs))
    except ValueError as e:
        raise SystemExit(str(e))
    print(f"Oluşturuldu: {os.path.relpath(path, ROOT)}")
    cmd_reindex()


def research_filename(meta):
    authors = meta.get("authors") or []
    first = ascii_slug(authors[0].split()[-1]) if authors else ""
    words = [w for w in ascii_slug(meta.get("title") or "untitled").split("-") if len(w) > 2][:4]
    short = "-".join(filter(None, [first] + words))[:48].strip("-")
    return f"{research_year(meta) or 'nd'}-{short or 'kayit'}.md"


def find_duplicate(tree, meta):
    keys = research_keys(meta)
    for r in tree.research:
        if keys & research_keys(r["meta"]):
            return r
    return None


def cmd_add_research(args):
    tree = Tree()
    if args.tech not in tree.nodes:
        raise SystemExit(f"Teknoloji bulunamadı: {args.tech}")
    meta = {"title": args.title, "authors": [a.strip() for a in args.authors.split(";") if a.strip()],
            "year": int(args.year) if args.year else None, "published_date": args.year,
            "doi": norm_doi(args.doi), "arxiv": norm_arxiv(args.arxiv), "url": args.url,
            "publication": args.publication, "publication_type": args.type or None,
            "peer_reviewed": {"yes": True, "no": False}.get(args.peer_reviewed),
            "primary_technology": args.tech, "related_technologies": split_list(args.related),
            "keywords": split_list(args.keywords)}
    dup = find_duplicate(tree, meta)
    if dup:
        raise SystemExit(f"Mükerrer kayıt: {dup['path']} ({research_id(dup['meta'])})")
    for t in meta["related_technologies"]:
        if t not in tree.nodes:
            raise SystemExit(f"İlişkili teknoloji bulunamadı: {t}")
    meta = {"research_id": research_id(meta), **meta, "classification_confidence": "high",
            "classification_method": "manual", "source_ids": ["manual"], "content_status": "metadata_only",
            "retraction_status": "unknown", "collected_at": date.today().isoformat(), "content_verified": False}
    rdir = os.path.join(ROOT, tree.nodes[args.tech]["dir"], RESEARCH_DIR)
    os.makedirs(rdir, exist_ok=True)
    fname = f"{args.year or 'nd'}-{args.short}.md" if args.short else research_filename(meta)
    path = os.path.join(rdir, fname)
    if os.path.exists(path):
        raise SystemExit(f"Dosya zaten var: {path}")
    links = [f"- DOI: https://doi.org/{meta['doi']}" if meta["doi"] else "",
             f"- arXiv: https://arxiv.org/abs/{meta['arxiv']}" if meta["arxiv"] else "",
             f"- URL: {args.url}" if args.url else ""]
    write(path, render_research(meta, {9: "\n".join(l for l in links if l)}))
    keep = os.path.join(rdir, ".gitkeep")
    if os.path.exists(keep):
        os.remove(keep)
    print(f"Oluşturuldu: {os.path.relpath(path, ROOT)} ({meta['research_id']})")
    cmd_reindex()


def cmd_find(args):
    tree = Tree(with_research=False)
    n = tree.nodes.get(args.id)
    print(n["dir"] if n else "bulunamadı")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="bilgi tabanı kökü (varsayılan: bu dosyanın iki üst dizini)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("reindex").set_defaults(fn=cmd_reindex)
    sub.add_parser("migrate-layout").set_defaults(fn=cmd_migrate_layout)
    p = sub.add_parser("check")
    p.add_argument("--verbose", action="store_true", help="tek çocuklu / yaprak alt disiplin notlarını da göster")
    p.set_defaults(fn=cmd_check)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    p = sub.add_parser("suggest")
    p.add_argument("text")
    p.add_argument("--limit", type=int, default=12)
    p.set_defaults(fn=cmd_suggest)
    p = sub.add_parser("find")
    p.add_argument("id")
    p.set_defaults(fn=cmd_find)
    p = sub.add_parser("add-tech")
    p.add_argument("--parent", required=True, help="üst teknoloji id (ana disiplin için 'root')")
    p.add_argument("--title", required=True, help="İngilizce ad")
    p.add_argument("--title-tr", help="Türkçe ad (klasör adı bundan türetilir)")
    p.add_argument("--id")
    p.add_argument("--slug")
    p.add_argument("--status", default="established", choices=["established", "emerging", "historical", "theoretical"])
    p.add_argument("--confidence", default="medium", choices=["high", "medium", "low"])
    p.add_argument("--aliases", default="")
    p.add_argument("--related", default="")
    p.add_argument("--depends-on", default="")
    p.add_argument("--applied-in", default="")
    p.add_argument("--refs", default="", help="sınıflandırma referansları, ör. arXiv:cs.CR")
    p.set_defaults(fn=cmd_add_tech)
    p = sub.add_parser("add-research")
    p.add_argument("--tech", required=True, help="en spesifik teknoloji id")
    p.add_argument("--title", required=True)
    p.add_argument("--authors", default="", help="noktalı virgülle ayrılmış")
    p.add_argument("--year")
    p.add_argument("--doi")
    p.add_argument("--arxiv")
    p.add_argument("--url")
    p.add_argument("--publication")
    p.add_argument("--type", default="", help="ör. article, preprint, review, standard, thesis")
    p.add_argument("--peer-reviewed", choices=["yes", "no"])
    p.add_argument("--related", default="", help="ilişkili teknoloji id'leri (virgülle)")
    p.add_argument("--keywords", default="")
    p.add_argument("--short", help="dosya adı kısa ad, ör. Groth16")
    p.set_defaults(fn=cmd_add_research)
    args = ap.parse_args(argv)
    if args.root:
        set_root(args.root)
    rc = args.fn(args)
    return rc if isinstance(rc, int) else 0


if __name__ == "__main__":
    sys.exit(main())
