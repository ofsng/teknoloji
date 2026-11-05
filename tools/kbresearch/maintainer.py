"""Knowledge Maintainer: `_index.md` bilgi bölümlerini kaynaklı biçimde doldurur ve güncelleme önerir.

İlkeler:
- Her ifade en az bir kaynağa bağlıdır; doğrulayıcı kaynaksız ya da bilinmeyen kaynaklı ifadeyi atar.
- Yalnızca BOŞ (yer tutucu) bölümler otomatik doldurulur; dolu bölümlere dokunulmaz, öneri dosyası yazılır.
- Yeni araştırma kaynaklı değişiklikler, çelişkiler ve geri çekmeler daima inceleme önerisidir.
- Ön baskıya dayanan ifadeler işaretlenir; content_verified yalnızca insan onayıyla true olur.
- Öncelik sırası: ana disiplinler → alt disiplinler → teknoloji aileleri → uzmanlaşmış yöntemler.
"""
import json
import os
import re
from datetime import date

import kb

from .state import load_json, save_json

FILL_SECTIONS = [1, 2, 3, 4, 5, 8, 9, 10, 11]
STMT = {"type": "object",
        "properties": {"text": {"type": "string"}, "sources": {"type": "array", "items": {"type": "string"}},
                       "basis": {"type": "string", "enum": ["review", "peer_reviewed", "preprint"]}},
        "required": ["text", "sources", "basis"], "additionalProperties": False}
DRAFT_SCHEMA = {"type": "object",
                "properties": {**{f"s{n}": {"type": "array", "items": STMT} for n in FILL_SECTIONS},
                               "conflicts": {"type": "array", "items": STMT}},
                "required": [f"s{n}" for n in FILL_SECTIONS] + ["conflicts"], "additionalProperties": False}
DRAFT_SYSTEM = (
    "You write sections of a Turkish-language technology knowledge base entry. You are given numbered sources "
    "(title, venue, year, whether peer reviewed, abstract). Write short Turkish statements ONLY from what these "
    "abstracts state. Every statement must cite the source ids it relies on. Do not add facts, numbers, dates or "
    "names that are not in the sources. If the sources do not support a section, return an empty list for it. "
    "Prefer review articles for definitions and principles. Mark basis=preprint when relying only on preprints. "
    "Put findings that disagree with each other into 'conflicts'. Sections: s1 definition, s2 working principle, "
    "s3 history, s4 key concepts, s5 key methods, s8 applications, s9 advantages, s10 limitations, "
    "s11 open problems. Use precise technical Turkish with English technical terms in parentheses where useful.")
UPDATE_SCHEMA = {"type": "object",
                 "properties": {"significant": {"type": "boolean"},
                                "change_type": {"type": "string", "enum": ["new_method", "limitation", "performance",
                                                                           "subtechnology", "contradiction",
                                                                           "application", "none"]},
                                "section": {"type": "integer"}, "proposed_text": {"type": "string"},
                                "contradicts": {"type": "array", "items": {"type": "string"}},
                                "rationale": {"type": "string"}},
                 "required": ["significant", "change_type", "section", "proposed_text", "contradicts", "rationale"],
                 "additionalProperties": False}
UPDATE_SYSTEM = (
    "You review whether a new paper (title + abstract only; the full text was not read) adds scientifically "
    "meaningful information to an existing Turkish knowledge-base entry. Most papers do not. Mark significant "
    "only for: a new technical method, a previously unknown limitation, a verified performance improvement, a new "
    "sub-technology, a contradiction with an existing statement, a new application, or a retraction-relevant fact. "
    "Never present a single new result as settled fact; phrase proposed_text in Turkish as a reported finding of "
    "this paper. List the existing statements it contradicts verbatim in 'contradicts'.")


def source_ref(s):
    who = (s.get("authors") or ["?"])[0]
    who = who + (" vd." if len(s.get("authors") or []) > 1 else "")
    link = f"https://doi.org/{s['doi']}" if s.get("doi") else (s.get("url") or "")
    kind = "hakemli" if s.get("peer_reviewed") is True else ("ön baskı" if s.get("peer_reviewed") is False else "tür belirsiz")
    return f"{who} ({s.get('year') or 'tarihsiz'}). *{s.get('title')}*. {s.get('publication') or ''}. {link} — {kind}"


def validate(draft, sources):
    """Kaynaksız / bilinmeyen kaynaklı / biçimsiz ifadeleri ayıklar. (temiz taslak, atılanlar)"""
    ids = {s["sid"] for s in sources}
    preprint = {s["sid"] for s in sources if s.get("peer_reviewed") is False}
    clean, dropped = {}, []
    for key in [f"s{n}" for n in FILL_SECTIONS] + ["conflicts"]:
        out = []
        for st in draft.get(key) or []:
            text = (st.get("text") or "").strip()
            srcs = [x for x in st.get("sources") or [] if x in ids]
            if not srcs or len(text) < 15 or len(text) > 700 or re.search(r"https?://", text):
                dropped.append({"section": key, "statement": st, "why": "kaynaksız/geçersiz"})
                continue
            basis = "preprint" if set(srcs) <= preprint else st.get("basis")
            out.append({"text": text, "sources": srcs, "basis": basis})
        clean[key] = out
    return clean, dropped


def render(clean, sources):
    """{bölüm no: markdown}, kaynak listesi markdown'u. Kaynak numaraları ilk kullanım sırasına göre."""
    order = []
    for key in [f"s{n}" for n in FILL_SECTIONS] + ["conflicts"]:
        for st in clean.get(key, []):
            for s in st["sources"]:
                if s not in order:
                    order.append(s)
    num = {s: i + 1 for i, s in enumerate(order)}
    by_sid = {s["sid"]: s for s in sources}
    out = {}
    for n in FILL_SECTIONS:
        items = clean.get(f"s{n}") or []
        if items:
            out[n] = "\n".join(f"- {st['text']}" + (" *(ön baskı bulgusu)*" if st["basis"] == "preprint" else "")
                               + " " + "".join(f"[{num[s]}]" for s in st["sources"]) for st in items)
    if clean.get("conflicts"):
        txt = "\n".join(f"- ⚖ {st['text']} " + "".join(f"[{num[s]}]" for s in st["sources"]) for st in clean["conflicts"])
        out[10] = (out.get(10, "") + "\n\n**Kaynaklar arasında uyuşmazlık:**\n" + txt).strip()
    refs = "\n".join(f"{num[s]}. {source_ref(by_sid[s])}" for s in order)
    return out, refs


def gather_sources(http, cfg, tree, nid, openalex, n_reviews=4, n_articles=3):
    """Düğüm için kaynaklar: önce derleme makaleleri, sonra çok atıf alan makaleler, sonra arşivdeki kayıtlar."""
    title = tree.nodes[nid]["meta"].get("title")
    seen, out = set(), []

    def add(rec):
        k = rec.get("doi") or rec.get("arxiv") or rec.get("title")
        if k in seen or not rec.get("abstract"):
            return
        seen.add(k)
        out.append({"sid": f"S{len(out) + 1}", "title": rec.get("title"), "authors": rec.get("authors"),
                    "year": (rec.get("published_date") or "")[:4], "doi": rec.get("doi"), "url": rec.get("url"),
                    "publication": rec.get("publication"), "peer_reviewed": rec.get("peer_reviewed"),
                    "type": rec.get("publication_type"), "abstract": rec.get("abstract")})
    for rec in openalex.search_top(http, cfg, title, n_reviews, types="review"):
        add(rec)
    for rec in openalex.search_top(http, cfg, title, n_articles, types="article"):
        add(rec)
    return out


def priority_queue(tree, limit, refresh=False):
    """Boş içerikli düğümler; sığdan derine, araştırma sayısı çok olan önce."""
    nodes = [n for n in tree.nodes.values()
             if refresh or (n["meta"].get("content_status") or "empty") in ("empty", "scope_note")]
    nodes.sort(key=lambda n: (n["depth"], -len(n["research"]), n["dir"]))
    return [n["id"] for n in nodes[:limit]]


def proposal_dir(cfg):
    return os.path.join(cfg.review_dir, "index-proposals")


def write_proposal(cfg, nid, kind, sections, sources_md, rationale, extra=None):
    d = proposal_dir(cfg)
    os.makedirs(d, exist_ok=True)
    base = f"{nid}--{cfg.today.isoformat()}--{kind}"
    path = os.path.join(d, base + ".md")
    i = 2
    while os.path.exists(path):
        path = os.path.join(d, f"{base}-{i}.md")
        i += 1
    meta = {"technology_id": nid, "kind": kind, "status": "pending", "created": cfg.today.isoformat(),
            "sections": sorted(sections), **(extra or {})}
    body = [f"# Öneri: {nid} — {kind}", "", "## Gerekçe", "", rationale.strip(), ""]
    for n, txt in sorted(sections.items()):
        body += [f"## {n}. {kb.SECTION_TITLES.get(n, '')}", "", txt.strip(), ""]
    if sources_md:
        body += ["## 14. Kaynaklar", "", sources_md.strip(), ""]
    kb.write(path, kb.dump_frontmatter(meta) + "\n" + "\n".join(body))
    return path


def apply_draft(cfg, tree, nid, clean, sources):
    """Boş bölümleri doldurur, dolu bölümler için öneri yazar. (doldurulan bölümler, öneri yolu)"""
    sections, refs = render(clean, sources)
    if not sections:
        return [], None
    path = os.path.join(kb.ROOT, tree.nodes[nid]["dir"], kb.INDEX)
    text = kb.read(path)
    meta, body = kb.parse_frontmatter(text)
    filled, blocked = [], {}
    for n, md in sections.items():
        cur = kb.get_section(body, n) or ""
        scope_only = n == 1 and cur.startswith("**Kapsam notu**")
        if kb.is_placeholder(cur) or scope_only:
            body = kb.replace_section(body, n, md + ("\n\n" + cur if scope_only else ""))
            filled.append(n)
        else:
            blocked[n] = md
    proposal = None
    if filled:
        cur14 = kb.get_section(body, 14) or ""
        if kb.is_placeholder(cur14):
            body = kb.replace_section(body, 14, refs)
        else:
            blocked[14] = refs
        meta["content_status"] = "ai_draft_sourced"
        meta["content_sources"] = [s.get("doi") or s.get("url") for s in sources
                                   if any(s["sid"] in st["sources"] for k in clean for st in clean[k])]
        meta["last_maintained"] = cfg.today.isoformat()
        meta["content_verified"] = False
        kb.write(path, kb.dump_frontmatter(meta) + "\n" + body)
    if blocked:
        proposal = write_proposal(cfg, nid, "fill", {k: v for k, v in blocked.items() if k != 14},
                                  blocked.get(14, refs),
                                  "Bu bölümlerde elle yazılmış ya da daha önce onaylanmış içerik var; "
                                  "otomatik üzerine yazılmadı.")
    return filled, proposal


def fill_node(cfg, tree, nid, llm=None, http=None, openalex=None, draft=None, sources=None):
    if sources is None:
        sources = gather_sources(http, cfg, tree, nid, openalex)
    if not sources:
        return {"node": nid, "status": "no_sources"}
    if draft is None:
        listing = "\n\n".join(
            f"[{s['sid']}] {s['title']} — {s.get('publication') or ''} ({s.get('year')}), "
            f"{'peer reviewed' if s.get('peer_reviewed') else ('preprint' if s.get('peer_reviewed') is False else 'unknown')}"
            f", type: {s.get('type')}\nAbstract: {s['abstract']}" for s in sources)
        n = tree.nodes[nid]
        path = " > ".join(tree.nodes[a]["meta"]["title"] for a in reversed(tree.ancestors(nid)))
        user = (f"Entry: {n['meta']['title']} ({n['meta']['title_tr']}); position in taxonomy: {path}.\n"
                f"Sub-technologies covered in their own entries (do not describe them in detail): "
                f"{', '.join(tree.nodes[c]['meta']['title'] for c in n['children']) or 'none'}.\n\nSources:\n{listing}")
        draft = llm.json_call("index_draft", DRAFT_SYSTEM, user, DRAFT_SCHEMA, max_tokens=16000, effort="medium")
    clean, dropped = validate(draft, sources)
    filled, proposal = apply_draft(cfg, tree, nid, clean, sources)
    return {"node": nid, "status": "filled" if filled else "nothing_filled", "filled": filled,
            "dropped": len(dropped), "proposal": proposal}


def assess_new_research(cfg, tree, nid, rmeta, abstract, llm):
    """Dolu bir _index.md için yeni araştırmanın anlamlı katkısı var mı? Varsa öneri dosyası (asla doğrudan yazmaz)."""
    path = os.path.join(kb.ROOT, tree.nodes[nid]["dir"], kb.INDEX)
    meta, body = kb.parse_frontmatter(kb.read(path))
    if (meta.get("content_status") or "empty") in ("empty", "scope_note") or not abstract:
        return None
    existing = "\n\n".join(f"## {n}. {kb.SECTION_TITLES[n]}\n{kb.get_section(body, n) or ''}" for n in FILL_SECTIONS
                           if not kb.is_placeholder(kb.get_section(body, n) or ""))
    peer = {True: "peer reviewed", False: "preprint (not peer reviewed)"}.get(rmeta.get("peer_reviewed"), "unknown")
    user = (f"Existing entry for {meta.get('title')}:\n{existing}\n\nNew paper ({peer}, {rmeta.get('published_date')}): "
            f"{rmeta.get('title')}\nAbstract: {abstract}")
    out = llm.json_call("index_update", UPDATE_SYSTEM, user, UPDATE_SCHEMA, max_tokens=6000, effort="medium")
    if not out.get("significant") or out.get("change_type") == "none":
        return None
    kind = "contradiction" if out.get("contradicts") else "update"
    ref = source_ref({"authors": rmeta.get("authors"), "year": rmeta.get("year"), "title": rmeta.get("title"),
                      "publication": rmeta.get("publication"), "doi": rmeta.get("doi"),
                      "url": rmeta.get("url"), "peer_reviewed": rmeta.get("peer_reviewed")})
    sec = out.get("section") if out.get("section") in FILL_SECTIONS else 13
    txt = f"- {out['proposed_text']} [yeni]"
    if out.get("contradicts"):
        txt += "\n\n**Çeliştiği mevcut ifadeler:**\n" + "\n".join(f"> {c}" for c in out["contradicts"])
    return write_proposal(cfg, nid, kind, {sec: txt}, f"[yeni] {ref}",
                          f"Değişiklik türü: {out['change_type']}. {out.get('rationale', '')} "
                          f"(Yalnızca başlık ve özet değerlendirildi.)",
                          {"research_id": rmeta.get("research_id")})


def retraction_proposals(cfg, tree, rmeta, notices):
    """Geri çekilen bir yayına dayanan _index.md içerikleri için deterministik öneri."""
    ids = {x for x in [rmeta.get("doi"), rmeta.get("url")] if x}
    out = []
    for nid, n in tree.nodes.items():
        if ids & set(n["meta"].get("content_sources") or []):
            det = "; ".join(f"{x.get('type')} ({x.get('notice_doi')}, {x.get('date')})" for x in notices)
            out.append(write_proposal(cfg, nid, "retraction", {}, "",
                                      f"Bu düğümün içeriği geri çekilen/düzeltilen bir yayına dayanıyor: "
                                      f"{rmeta.get('title')} ({rmeta.get('doi')}). Bildirim: {det}. "
                                      f"İlgili ifadeler gözden geçirilmeli.", {"research_id": rmeta.get("research_id")}))
    return out


def list_proposals(cfg, status="pending"):
    d = proposal_dir(cfg)
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".md"):
            m, _ = kb.parse_frontmatter(kb.read(os.path.join(d, f)))
            if status is None or m.get("status") == status:
                out.append((os.path.join(d, f), m))
    return out


def apply_proposal(cfg, tree, path):
    """İnsan onayıyla öneriyi uygula: metni ilgili bölüme ekler (mevcut içerik korunur)."""
    pm, pbody = kb.parse_frontmatter(kb.read(path))
    if pm.get("status") != "pending":
        raise ValueError("Öneri bekleyen durumda değil")
    nid = pm["technology_id"]
    ipath = os.path.join(kb.ROOT, tree.nodes[nid]["dir"], kb.INDEX)
    meta, body = kb.parse_frontmatter(kb.read(ipath))
    for n, _, content in kb.split_sections(pbody)[1]:
        if n == 14 or not content.strip():
            continue
        cur = kb.get_section(body, n) or ""
        body = kb.replace_section(body, n, content if kb.is_placeholder(cur) else cur + "\n" + content)
    refs = kb.get_section(pbody, 14)
    if refs:
        cur = kb.get_section(body, 14) or ""
        body = kb.replace_section(body, 14, refs if kb.is_placeholder(cur) else cur + "\n" + refs)
    meta["last_maintained"] = cfg.today.isoformat()
    kb.write(ipath, kb.dump_frontmatter(meta) + "\n" + body)
    pm["status"] = "applied"
    pm["applied"] = cfg.today.isoformat()
    kb.write(path, kb.dump_frontmatter(pm) + "\n" + pbody)


def set_proposal_status(path, status):
    pm, pbody = kb.parse_frontmatter(kb.read(path))
    pm["status"] = status
    kb.write(path, kb.dump_frontmatter(pm) + "\n" + pbody)
