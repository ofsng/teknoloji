#!/usr/bin/env python3
"""Technology-Knowledge-Base bakım aracı (yalnızca Python standart kütüphanesi).

Kaynak gerçeklik: klasör ağacı ve her klasördeki `_index.md` ön bilgisi (frontmatter).
`tools/seed/*.tax` dosyaları ilk kurulumda kullanılan taksonomi tanımlarıdır; `build`
yalnızca eksik klasörleri/dosyaları oluşturur, mevcut içeriğin üzerine yazmaz
(yalnızca `<!-- AUTO:BEGIN -->` ... `<!-- AUTO:END -->` blokları yenilenir).

Komutlar:
  build                 Seed dosyalarından eksik klasörleri ve _index.md dosyalarını oluştur, sonra reindex.
  reindex               AUTO bloklarını ve merkezi indeksleri yeniden üret.
  check                 Doğrulama: kırık bağlantı, mükerrer teknoloji/DOI/arXiv, hiyerarşi, yetim klasör.
  stats                 Sayım raporu.
  suggest "metin"       Yeni bir teknoloji için olası üst konumları öner.
  add-tech              Yeni teknoloji klasörü ekle.
  add-research          Bir teknolojiye araştırma kaydı ekle (mükerrer kontrolüyle).
  find ID               Bir teknoloji kimliğinin yolunu göster.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(ROOT, "tools", "seed")
INDEX = "_index.md"
RESEARCH_DIR = "Arastirmalar"
SKIP_DIRS = {"tools", "templates", RESEARCH_DIR}
AUTO_BEGIN = "<!-- AUTO:BEGIN (kb.py reindex üretir; bu bloğu elle düzenlemeyin) -->"
AUTO_END = "<!-- AUTO:END -->"
AUTO_RE = re.compile(r"<!-- AUTO:BEGIN.*?-->.*?<!-- AUTO:END -->", re.S)
REL_KEYS = [("related", "İlişkili (Related)"), ("depends_on", "Bağımlı olduğu (Depends on)"),
            ("applied_in", "Kullanıldığı alanlar (Applied in)")]

TR_MAP = str.maketrans({"ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I",
                        "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U",
                        "â": "a", "Â": "A", "î": "i", "û": "u"})


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
    if isinstance(v, int):
        return str(v)
    s = str(v)
    if re.fullmatch(r"[A-Za-z0-9_.:/-]+", s) and s not in ("true", "false", "null"):
        return s
    return json.dumps(s, ensure_ascii=False)


def dump_frontmatter(meta):
    return "---\n" + "".join(f"{k}: {dump_value(v)}".rstrip() + "\n" for k, v in meta.items()) + "---\n"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


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


SECTIONS = ["## 1. Tanım", "## 2. Temel çalışma prensibi", AUTO_BEGIN + "\n" + AUTO_END,
            "## 6. Temel teknik kavramlar", "## 7. Önemli tarihsel gelişmeler",
            "## 8. Başlıca araştırma konuları", "## 9. Açık teknik problemler", "## 10. Kaynaklar"]
PLACEHOLDER = "_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._"


def new_index_text(meta, definition=None):
    body = [f"# {meta['title_tr']}" + (f" ({meta['title']})" if meta["title"] != meta["title_tr"] else ""), ""]
    for sec in SECTIONS:
        body.append(sec)
        if sec.startswith("## "):
            body.append("")
            body.append(definition if (sec.startswith("## 1.") and definition) else PLACEHOLDER)
        body.append("")
    return dump_frontmatter(meta) + "\n" + "\n".join(body)


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
            "aliases": split_list(o.get("alias", "").replace("/", ",")),
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
    def __init__(self):
        self.nodes = {}          # id -> node dict
        self.by_path = {}        # rel dir -> id
        self.orphans = []        # dirs without _index.md
        self.dup_ids = []
        self.research = []
        self.top = []
        self.scan()

    def scan(self):
        for dirpath, dirnames, filenames in os.walk(ROOT):
            rel = os.path.relpath(dirpath, ROOT)
            dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")) and
                                 not (rel == "." and d in SKIP_DIRS) and d != RESEARCH_DIR)
            if os.path.basename(dirpath) == RESEARCH_DIR:
                continue
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
            if os.path.isdir(rdir):
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

    def walk(self):
        def rec(nid):
            yield nid
            for c in self.nodes[nid]["children"]:
                yield from rec(c)
        for t in self.top:
            yield from rec(t)


# ---------------------------------------------------------------- reindex

def auto_block(tree, nid):
    n = tree.nodes[nid]
    d = n["dir"]
    crumbs = []
    cur = n["parent_id"]
    while cur not in ("root", None):
        crumbs.append(tree.link(d, cur))
        cur = tree.nodes[cur]["parent_id"]
    home = os.path.relpath("TECHNOLOGIES.md", d).replace(os.sep, "/")
    out = [AUTO_BEGIN, "", f"**Konum:** [Kök]({home}) › " + " › ".join(list(reversed(crumbs)) + [f"**{tree.name(nid)}**"]),
           "", "## 3. Üst teknoloji", ""]
    out.append(f"- {tree.link(d, n['parent_id'])}" if n["parent_id"] not in ("root", None)
               else f"- Ana disiplin (kök: [TECHNOLOGIES.md]({home}))")
    out += ["", "## 4. Alt teknolojiler", ""]
    out += [f"- {tree.link(d, c)}" for c in n["children"]] or ["- _Yaprak düğüm (alt sınıflandırma yok)._"]
    out += ["", "## 5. İlişkili teknolojiler", ""]
    any_rel = False
    for key, label in REL_KEYS:
        targets = n["meta"].get(key) or []
        if targets:
            any_rel = True
            items = [tree.link(d, t) if t in tree.nodes else f"`{t}` (bulunamadı)" for t in targets]
            out.append(f"- **{label}:** " + ", ".join(items))
    if n["incoming"]:
        any_rel = True
        seen = []
        for src, _ in n["incoming"]:
            if src not in seen:
                seen.append(src)
        out.append("- **Bu teknolojiye bağlananlar:** " + ", ".join(tree.link(d, s) for s in seen))
    if not any_rel:
        out.append("- _Tanımlı ilişki yok._")
    out += ["", f"**Araştırma kayıtları:** {len(n['research'])}"
            + (f" — [{RESEARCH_DIR}/]({RESEARCH_DIR}/)" if n["research"] else f" (`{RESEARCH_DIR}/` klasörüne eklenir)")]
    for r in n["research"]:
        rel = os.path.relpath(r["path"], d).replace(os.sep, "/")
        out.append(f"- [{r['meta'].get('title') or os.path.basename(r['path'])}]({rel})")
    out += ["", AUTO_END]
    return "\n".join(out)


def cmd_reindex(args=None):
    tree = Tree()
    changed = 0
    for nid in tree.nodes:
        path = os.path.join(ROOT, tree.nodes[nid]["dir"], INDEX)
        text = read(path)
        block = auto_block(tree, nid)
        new = AUTO_RE.sub(lambda _: block, text, count=1) if AUTO_RE.search(text) else text.rstrip() + "\n\n" + block + "\n"
        if new != text:
            write(path, new)
            changed += 1
    write_technologies(tree)
    write_research_index(tree)
    write_relationships(tree)
    write_stats(tree)
    update_taxonomy_table(tree)
    print(f"reindex: {len(tree.nodes)} teknoloji düğümü, {changed} _index.md güncellendi, {len(tree.research)} araştırma")


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


def write_research_index(tree):
    lines = ["# Araştırma İndeksi", "", GEN_NOTE,
             f"Toplam kayıt: **{len(tree.research)}**", ""]
    if tree.research:
        lines += ["| Yıl | Başlık | Kimlik | Teknoloji | Tür |", "|---|---|---|---|---|"]
        for r in sorted(tree.research, key=lambda r: (str(r["meta"].get("year") or ""), r["path"])):
            m = r["meta"]
            title = (m.get("title") or os.path.basename(r["path"])).replace("|", "\\|")
            rid = m.get("research_id") or research_id(m)
            lines.append(f"| {m.get('year') or ''} | [{title}]({r['path'].replace(os.sep, '/')}) | `{rid}` | "
                         f"{tree.link('.', r['tech'])} | {m.get('research_type') or ''} |")
    else:
        lines.append("_Henüz araştırma kaydı yok. Eklemek için: `python3 tools/kb.py add-research --help`_")
    write(os.path.join(ROOT, "RESEARCH-INDEX.md"), "\n".join(lines) + "\n")


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
    leaves = sum(1 for n in tree.nodes.values() if not n["children"])
    per_top = {t: sum(1 for _ in subtree(tree, t)) for t in tree.top}
    return {"disciplines": len(tree.top), "nodes": len(tree.nodes),
            "technologies": len(tree.nodes) - len(tree.top), "leaves": leaves,
            "dirs_total": dirs, "md_files": md, "max_depth": depth,
            "depth_hist": dict(sorted(depth_hist.items())), "research": len(tree.research),
            "relations": sum(len(n["meta"].get(k) or []) for n in tree.nodes.values() for k, _ in REL_KEYS),
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
             f"- Tanımlı ilişki: **{s['relations']}**", "",
             "## Derinlik dağılımı", "", "| Seviye | Düğüm |", "|---|---|"]
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
    rows = [AUTO_BEGIN, "", "| Ana disiplin | Klasör | Düğüm | Sınıflandırma referansları |", "|---|---|---|---|"]
    for t in tree.top:
        refs = ", ".join(tree.nodes[t]["meta"].get("classification_refs") or [])
        rows.append(f"| {tree.link('.', t)} | `{tree.nodes[t]['dir']}/` | {sum(1 for _ in subtree(tree, t))} | {refs} |")
    rows += ["", AUTO_END]
    write(path, AUTO_RE.sub(lambda _: "\n".join(rows), text, count=1))


# ---------------------------------------------------------------- research ids

def research_id(meta):
    doi = (meta.get("doi") or "").strip().lower()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)
    if doi:
        return f"doi:{doi}"
    ax = (meta.get("arxiv") or "").strip().lower()
    ax = re.sub(r"^(arxiv:|https?://arxiv\.org/abs/)", "", ax)
    ax = re.sub(r"v\d+$", "", ax)
    if ax:
        return f"arxiv:{ax}"
    authors = meta.get("authors") or []
    first = norm_title(authors[0].split()[-1]) if authors else "anon"
    key = f"{norm_title(meta.get('title') or '')}|{meta.get('year') or ''}|{first}"
    return f"kb:{meta.get('year') or 'nd'}-{first}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"


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
        if m.get("id") and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", m["id"]):
            errors.append(f"{n['dir']}: id biçimi geçersiz: {m['id']}")
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
        if n["meta"].get("type") == "discipline" and not n["children"]:
            warnings.append(f"{n['dir']}: ana disiplin fakat alt düğümü yok")
        if n["meta"].get("type") == "subdiscipline" and not n["children"]:
            infos.append(f"{n['dir']}: yaprak alt disiplin")
        if len(n["children"]) == 1:
            infos.append(f"{n['dir']}: tek çocuklu düğüm (gerçek alt tür mü, gereksiz derinlik mi gözden geçirin)")
        if len(os.path.join("Technology-Knowledge-Base", n["dir"], INDEX)) > 240:
            warnings.append(f"{n['dir']}: yol 240 karakteri aşıyor (Windows uyumluluğu)")
    for k, ids in titles.items():
        uniq = sorted(set(ids))
        if len(uniq) > 1:
            errors.append(f"Olası mükerrer teknoloji (aynı ad '{k}'): " + ", ".join(tree.nodes[i]["dir"] for i in uniq))
    # Takma ad başka bir teknolojinin adıysa: iki klasör aynı kavramı temsil ediyor olabilir
    for nid, n in tree.nodes.items():
        for a in n["meta"].get("aliases") or []:
            for other in titles.get(norm_title(a), []):
                if other != nid and not is_ancestor(tree, other, nid) and not is_ancestor(tree, nid, other):
                    warnings.append(f"{n['dir']}: takma ad '{a}' başka bir teknolojinin adı: {tree.nodes[other]['dir']}")
    # research duplicates
    seen = defaultdict(list)
    for r in tree.research:
        m = r["meta"]
        rid = research_id(m)
        seen[rid].append(r["path"])
        if m.get("research_id") and m["research_id"] != rid:
            warnings.append(f"{r['path']}: research_id ({m['research_id']}) hesaplanan kimlikle ({rid}) uyuşmuyor")
        if m.get("arxiv") and rid.startswith("doi:"):
            seen["arxiv:" + re.sub(r"v\d+$", "", str(m["arxiv"]).lower().replace("arxiv:", ""))].append(r["path"])
        seen["title:" + norm_title(m.get("title") or "") + str(m.get("year"))].append(r["path"])
        if m.get("technology_id") != r["tech"]:
            errors.append(f"{r['path']}: technology_id='{m.get('technology_id')}' fakat klasör '{r['tech']}'")
        for t in m.get("related_technologies") or []:
            if t not in tree.nodes:
                errors.append(f"{r['path']}: related_technologies hedefi bulunamadı: {t}")
    for k, paths in seen.items():
        if len(set(paths)) > 1:
            errors.append(f"Mükerrer araştırma ({k}): " + ", ".join(sorted(set(paths))))
    # broken links
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
    if args.verbose:
        for i in infos:
            print("BİLGİ:", i)
    for w in warnings:
        print("UYARI:", w)
    for e in errors:
        print("HATA:", e)
    print(f"\ncheck: {s['nodes']} düğüm, {s['research']} araştırma, {len(errors)} hata, {len(warnings)} uyarı, "
          f"{len(infos)} bilgi notu" + ("" if args.verbose else " (görmek için --verbose)"))
    return 1 if errors else 0


def is_ancestor(tree, anc, nid):
    cur = tree.nodes[nid]["parent_id"]
    while cur not in ("root", None):
        if cur == anc:
            return True
        cur = tree.nodes[cur]["parent_id"]
    return False


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
    tree = Tree()
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


def cmd_add_tech(args):
    tree = Tree()
    if args.parent not in tree.nodes and args.parent != "root":
        raise SystemExit(f"Üst teknoloji bulunamadı: {args.parent} (öneri için: kb.py suggest)")
    nid = args.id or make_id(args.title)
    if nid in tree.nodes:
        raise SystemExit(f"Bu id zaten var: {nid} -> {tree.nodes[nid]['dir']}")
    for other in tree.nodes.values():
        if norm_title(args.title) in (norm_title(other["meta"].get("title", "")), norm_title(other["meta"].get("title_tr", ""))):
            raise SystemExit(f"Aynı adlı teknoloji zaten var: {other['dir']}")
    parent_dir = tree.nodes[args.parent]["dir"] if args.parent != "root" else ""
    slug = args.slug or ascii_slug(args.title_tr or args.title)
    path = os.path.join(ROOT, parent_dir, slug)
    if os.path.exists(path):
        raise SystemExit(f"Klasör zaten var: {path}")
    depth = len(os.path.relpath(path, ROOT).split(os.sep))
    os.makedirs(os.path.join(path, RESEARCH_DIR))
    write(os.path.join(path, RESEARCH_DIR, ".gitkeep"), "")
    meta = {"id": nid, "title": args.title, "title_tr": args.title_tr or args.title, "type": node_type(depth),
            "parent": args.parent, "status": args.status, "classification_confidence": args.confidence,
            "aliases": split_list(args.aliases), "related": split_list(args.related),
            "depends_on": split_list(args.depends_on), "applied_in": split_list(args.applied_in),
            "classification_refs": split_list(args.refs), "content_verified": False,
            "created": date.today().isoformat()}
    write(os.path.join(path, INDEX), new_index_text(meta))
    print(f"Oluşturuldu: {os.path.relpath(path, ROOT)}")
    cmd_reindex()


RESEARCH_TEMPLATE = """
# {title}

## 1. Araştırmanın amacı

{ph}

## 2. Ele aldığı problem

{ph}

## 3. Kullanılan yöntem

{ph}

## 4. Temel bulgular

{ph}

## 5. Teknik katkıları

{ph}

## 6. Sınırlılıkları

{ph}

## 7. İlişkili çalışmalar

{ph}

## 8. Kaynak bağlantıları

{links}
"""


def cmd_add_research(args):
    tree = Tree()
    if args.tech not in tree.nodes:
        raise SystemExit(f"Teknoloji bulunamadı: {args.tech}")
    meta = {"title": args.title, "authors": [a.strip() for a in args.authors.split(";") if a.strip()],
            "year": int(args.year) if args.year else None, "doi": args.doi, "arxiv": args.arxiv,
            "url": args.url, "publication": args.publication, "research_type": args.type,
            "technology_id": args.tech, "related_technologies": split_list(args.related),
            "keywords": split_list(args.keywords)}
    rid = research_id(meta)
    for r in tree.research:
        if research_id(r["meta"]) == rid or (norm_title(r["meta"].get("title") or "") == norm_title(args.title)
                                             and str(r["meta"].get("year")) == str(args.year)):
            raise SystemExit(f"Mükerrer kayıt: {r['path']} ({rid})")
    for t in meta["related_technologies"]:
        if t not in tree.nodes:
            raise SystemExit(f"İlişkili teknoloji bulunamadı: {t}")
    meta = {"research_id": rid, **meta, "added": date.today().isoformat(), "content_verified": False}
    short = args.short or ascii_slug(args.title)[:40].strip("-")
    fname = f"{args.year or 'nd'}-{short}.md"
    rdir = os.path.join(ROOT, tree.nodes[args.tech]["dir"], RESEARCH_DIR)
    os.makedirs(rdir, exist_ok=True)
    path = os.path.join(rdir, fname)
    if os.path.exists(path):
        raise SystemExit(f"Dosya zaten var: {path}")
    links = [f"- DOI: https://doi.org/{args.doi}" if args.doi else "", f"- arXiv: https://arxiv.org/abs/{args.arxiv}" if args.arxiv else "",
             f"- URL: {args.url}" if args.url else ""]
    write(path, dump_frontmatter(meta) + RESEARCH_TEMPLATE.format(
        title=args.title, ph=PLACEHOLDER, links="\n".join(l for l in links if l) or PLACEHOLDER))
    keep = os.path.join(rdir, ".gitkeep")
    if os.path.exists(keep):
        os.remove(keep)
    print(f"Oluşturuldu: {os.path.relpath(path, ROOT)} ({rid})")
    cmd_reindex()


def cmd_find(args):
    tree = Tree()
    n = tree.nodes.get(args.id)
    print(n["dir"] if n else "bulunamadı")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("reindex").set_defaults(fn=cmd_reindex)
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
    p.add_argument("--type", default="", help="ör. original, survey, benchmark, standard, thesis")
    p.add_argument("--related", default="", help="ilişkili teknoloji id'leri (virgülle)")
    p.add_argument("--keywords", default="")
    p.add_argument("--short", help="dosya adı kısa ad, ör. Groth16")
    p.set_defaults(fn=cmd_add_research)
    args = ap.parse_args()
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
