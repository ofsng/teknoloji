"""Tanıtım kartı (_tanitim.md) üretimi. Biçim: templates/tanitim.template.md, denetim: kb.check_intro.

İki adım:
1. Kaynak paketi (packet): düğümü anlatan çalışmalar OpenAlex'ten (önce derlemeler, bağlam denetimiyle) çekilir;
   künye ve özetler .cache/intro/<id>.json dosyasına yazılır.
2. Yanıt (answer): bir yazar (Claude API ya da oturumdaki insan/model) yalnızca paketteki özetlere dayanarak
   yapılandırılmış JSON yazar; her ifade paket kaynak numaralarına bağlanır.

Kaynaklar bölümü yanıttan değil paketten üretilir: yazar kaynak uyduramaz. Paket dışı numaraya bağlı ya da
kaynaksız ifadeler atılır; boşalan blok boş kalır. Var olan _tanitim.md'nin üzerine yazılmaz.
"""
import json
import os
import re
import urllib.parse

import kb
from .pipeline import context_phrases, has_context
from .sources import openalex
from .http import SourceUnavailable

CACHE = ".cache/intro"
PER_NODE = 6
ABSTRACT_CHARS = 1800

SYSTEM = """Bir bilim ve teknoloji atlası için Türkçe, kısa ve net tanıtım kartı yazıyorsun.
Kurallar:
- Yalnızca verilen kaynak özetlerinde açıkça geçen bilgileri kullan. Kendi bilgini, tahminini ya da özetlerde
  olmayan yıl/sayı/adı ekleme. Bir blok için özetlerde bilgi yoksa o bloğu boş dizi/boş metin bırak.
- Her ifadeye dayandığı kaynak numaralarını "kaynaklar" alanında ver (yalnızca verilen numaralar).
- Wikipedia üslubu değil: sade, güncel, akıcı Türkçe; jargon gerekiyorsa kısaca aç. Abartı ve pazarlama dili yok.
- oz: tek cümle, en çok 25 kelime, "bu alan nedir?" sorusunun cevabı.
- neden: 1-2 cümle, alan neyi değiştirdi / neden önemli.
- gecmis: en çok 4 kilometre taşı; etiket yıl (YYYY) olmalı ve yıl özette açıkça geçmeli; yoksa gecmis boş.
  Ana disiplinlerde gecmis yerine ana kollar: etiket kolun kısa adı, metin kapsamı.
- bugun: 2-4 kısa kullanım alanı etiketi (2-5 kelime).
- beklenen: 1-3 madde; yalnızca özetlerde açık problem, zorluk ya da gelecek yönü olarak geçenler.
- Toplam 120-180 kelime hedefle. Kaynaklar konuyla ilgisizse ilgili olmayanı kullanma."""

ITEM = {"type": "object", "additionalProperties": False, "required": ["etiket", "metin", "kaynaklar"],
        "properties": {"etiket": {"type": "string"}, "metin": {"type": "string"},
                       "kaynaklar": {"type": "array", "items": {"type": "integer"}}}}
CLAIM = {"type": "object", "additionalProperties": False, "required": ["metin", "kaynaklar"],
         "properties": {"metin": {"type": "string"}, "kaynaklar": {"type": "array", "items": {"type": "integer"}}}}
SCHEMA = {"type": "object", "additionalProperties": False,
          "required": ["oz", "neden", "gecmis", "bugun", "beklenen"],
          "properties": {"oz": CLAIM, "neden": {"type": "array", "items": CLAIM},
                         "gecmis": {"type": "array", "items": ITEM},
                         "bugun": {"type": "array", "items": CLAIM}, "beklenen": {"type": "array", "items": CLAIM}}}


def packet_path(nid):
    return os.path.join(kb.ROOT, CACHE, f"{nid}.json")


def answer_path(nid):
    return os.path.join(kb.ROOT, CACHE, f"{nid}.answer.json")


def node_info(tree, nid):
    n = tree.nodes[nid]
    m = n["meta"]
    return {"id": nid, "title": m.get("title"), "title_tr": m.get("title_tr"), "type": m.get("type"),
            "status": m.get("status"), "aliases": list(m.get("aliases") or []),
            "path": [tree.nodes[a]["meta"].get("title_tr") for a in reversed(tree.ancestors(nid)) if a in tree.nodes],
            "children": [tree.nodes[c]["meta"].get("title_tr") for c in n["children"]]}


def fetch_packet(http, cfg, tree, nid, n=PER_NODE):
    """Düğümü anlatan, bağlamı tutan, özeti olan en çok n çalışma (DOI'li)."""
    title = tree.nodes[nid]["meta"].get("title")
    ctx = context_phrases(tree, nid)
    seen, sources = set(), []
    for rec in openalex.search_explainers(http, cfg, title, n * 2):
        doi = kb.norm_doi(rec.get("doi"))
        if not doi or doi in seen or not rec.get("abstract") or not has_context(rec, ctx):
            continue
        seen.add(doi)
        sources.append({"n": len(sources) + 1, "doi": doi, "title": rec.get("title"),
                        "year": (rec.get("published_date") or "")[:4] or None,
                        "authors": (rec.get("authors") or [])[:3], "authors_more": len(rec.get("authors") or []) > 3,
                        "venue": rec.get("publication"), "type": rec.get("publication_type"),
                        "abstract": (rec.get("abstract") or "")[:ABSTRACT_CHARS]})
        if len(sources) >= n:
            break
    return {"node": node_info(tree, nid), "sources": sources}


def save_packet(nid, packet):
    os.makedirs(os.path.dirname(packet_path(nid)), exist_ok=True)
    with open(packet_path(nid), "w", encoding="utf-8") as f:
        json.dump(packet, f, ensure_ascii=False, indent=1)


def user_prompt(packet):
    node = packet["node"]
    lines = [f"Düğüm: {node['title_tr']} ({node['title']}) — tür: {node['type']}, durum: {node['status']}",
             "Konum: " + " › ".join(node["path"] + [node["title_tr"]]),
             "Alt alanlar: " + (", ".join(node["children"]) or "yok"),
             "Ana disiplin: gecmis alanına ana kolları yaz." if node["type"] == "discipline" else "", "",
             "Kaynaklar:"]
    for s in packet["sources"]:
        lines.append(f"[{s['n']}] {s['title']} ({s['year']}, {s['venue']}, {s['type']})\nÖzet: {s['abstract']}\n")
    return "\n".join(lines)


def write_with_llm(llm, packet):
    return llm.json_call("intro", SYSTEM, user_prompt(packet), SCHEMA, max_tokens=4000, effort="medium")


def _authors(s):
    names = [a.split()[-1] if a else "?" for a in s["authors"]]
    if not names:
        return "Yazar belirtilmemiş"
    if s["authors_more"] or len(names) > 2:
        return f"{names[0]} vd."
    return ", ".join(names)


def _cite(nums, valid):
    nums = sorted({int(x) for x in nums if int(x) in valid})
    return f" [{', '.join(map(str, nums))}]" if nums else ""


def _clean(text):
    return re.sub(r"\s*\[\d+(?:\s*,\s*\d+)*\]", "", (text or "").strip()).strip()


def render(packet, answer, today, written_by):
    """Yanıt + paket → _tanitim.md metni. Kaynaksız ya da paket dışı numaralı ifadeler atılır;
    yalnızca kullanılan kaynaklar listelenir ve yeniden numaralanır."""
    node, srcs = packet["node"], packet["sources"]
    valid = {s["n"] for s in srcs}

    def ok(c):
        return _clean(c.get("metin")) and any(int(x) in valid for x in c.get("kaynaklar") or [])

    oz = answer.get("oz") or {}
    oz = [oz] if ok(oz) else []
    neden = [c for c in answer.get("neden") or [] if ok(c)]
    past = [c for c in answer.get("gecmis") or [] if ok(c) and _clean(c.get("etiket"))]
    if node["type"] != "discipline":
        past = [c for c in past if re.fullmatch(r"\d{4}", c["etiket"].strip())]
    bugun = [c for c in answer.get("bugun") or [] if ok(c)]
    beklenen = [c for c in answer.get("beklenen") or [] if ok(c)]
    if not oz:
        return None
    used = sorted({int(x) for c in oz + neden + past + bugun + beklenen for x in c["kaynaklar"] if int(x) in valid})
    renum = {old: i + 1 for i, old in enumerate(used)}

    def cite(c):
        return _cite([renum[int(x)] for x in c["kaynaklar"] if int(x) in renum], set(renum.values()))

    def sentence(c):
        t = _clean(c["metin"])
        return t if t.endswith((".", "!", "?")) else t + "."

    out = ["---", f"node: {node['id']}", "intro_status: ai_draft_sourced", "intro_version: 1",
           f"written: {today}", f"written_by: {json.dumps(written_by, ensure_ascii=False)}", "human_verified: false",
           "---", "", "## Öz", "", sentence(oz[0]) + cite(oz[0]), "", "## Neden önemli", ""]
    if neden:
        out += [" ".join(sentence(c) + cite(c) for c in neden), ""]
    out += ["## " + ("Ana kollar" if node["type"] == "discipline" else "Neler yapıldı"), ""]
    out += [f"- **{_clean(c['etiket'])}** · {sentence(c)}{cite(c)}" for c in past] + ([""] if past else [])
    out += ["## Bugün nerede", ""] + [f"- {_clean(c['metin']).rstrip('.')}{cite(c)}" for c in bugun] + ([""] if bugun else [])
    out += ["## Neler bekleniyor", ""] + [f"- {sentence(c)}{cite(c)}" for c in beklenen] + ([""] if beklenen else [])
    out += ["## Kaynaklar", ""]
    for old in used:
        s = next(x for x in srcs if x["n"] == old)
        venue = f" {s['venue']}." if s.get("venue") else ""
        out.append(f"{renum[old]}. {_authors(s)} ({s['year'] or 't.y.'}). {_clean(s['title'])}.{venue} https://doi.org/{urllib.parse.quote(s['doi'], safe='/:;()._-')}")
    return "\n".join(out) + "\n"


def target_ids(tree, ids=None, depth=None, limit=None):
    """Tanıtımı olmayan düğümler; derinlik sonra kimlik sırasıyla (deterministik)."""
    pool = ids or sorted(tree.nodes, key=lambda i: (tree.nodes[i]["depth"], tree.nodes[i]["dir"]))
    out = [i for i in pool if i in tree.nodes and not os.path.exists(os.path.join(kb.ROOT, tree.nodes[i]["dir"], kb.INTRO))
           and (depth is None or tree.nodes[i]["depth"] == depth)]
    return out[:limit] if limit else out


def run(cfg, http, llm, ids=None, depth=None, limit=None, packets_only=False, from_answers=False,
        written_by="Claude (yapay zekâ taslağı; yalnızca OpenAlex kaynak özetlerine dayanır)", log=print):
    tree = kb.Tree(with_research=False)
    stats = {"packets": 0, "no_sources": [], "written": [], "rejected": [], "skipped_no_answer": 0, "errors": []}
    for nid in target_ids(tree, ids, depth, limit):
        packet = None
        if os.path.exists(packet_path(nid)):
            with open(packet_path(nid), encoding="utf-8") as f:
                packet = json.load(f)
        elif not from_answers:
            try:
                packet = fetch_packet(http, cfg, tree, nid)
            except (SourceUnavailable, ValueError) as e:
                stats["errors"].append(f"{nid}: {e}")
                break
            save_packet(nid, packet)
            stats["packets"] += 1
        if packet is None:
            continue
        if not packet["sources"]:
            stats["no_sources"].append(nid)
            continue
        if packets_only:
            continue
        if from_answers:
            if not os.path.exists(answer_path(nid)):
                stats["skipped_no_answer"] += 1
                continue
            with open(answer_path(nid), encoding="utf-8") as f:
                answer = json.load(f)
        else:
            answer = write_with_llm(llm, packet)
        text = render(packet, answer, cfg.today.isoformat(), written_by)
        errs = kb.check_intro(text, tree.nodes[nid])[0] if text else ["öz yok"]
        if errs:
            stats["rejected"].append(f"{nid}: {errs[0]}")
            continue
        kb.write(os.path.join(kb.ROOT, tree.nodes[nid]["dir"], kb.INTRO), text)
        stats["written"].append(nid)
        log(f"tanıtım: {nid}")
    return stats
