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
        "properties": {"text": {"type": "string"},
                       "evidence": {"type": "string"},
                       "sources": {"type": "array", "items": {"type": "string"}},
                       "basis": {"type": "string", "enum": ["review", "peer_reviewed", "preprint"]}},
        "required": ["text", "evidence", "sources", "basis"], "additionalProperties": False}
DRAFT_SCHEMA = {"type": "object",
                "properties": {**{f"s{n}": {"type": "array", "items": STMT} for n in FILL_SECTIONS},
                               "conflicts": {"type": "array", "items": STMT}},
                "required": [f"s{n}" for n in FILL_SECTIONS] + ["conflicts"], "additionalProperties": False}
DRAFT_SYSTEM = (
    "You write sections of a Turkish-language technology knowledge base entry. You are given numbered sources "
    "(title, venue, year, whether peer reviewed, abstract). Write short Turkish statements ONLY from what these "
    "abstracts state. Every statement must cite the source ids it relies on and must include 'evidence': an "
    "EXACT, verbatim English quote (8 to 40 words, copied character for character) from the abstract of the first "
    "cited source that supports the statement, and the quote must name this technology. 'text' MUST be written in "
    "Turkish and be a faithful Turkish rendering of the quote: keep technical terms in English in parentheses, do "
    "not add, generalize or change meaning, and never copy English into 'text'. Do not add "
    "facts, numbers, dates or names that are not in the quote. If the sources do not support a section, return an "
    "empty list for it. Prefer fewer, accurate statements over many. "
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


def _norm(t):
    t = (t or "").lower()
    t = re.sub(r"[‐-―−]", "-", t)
    t = re.sub(r"[“”\"'‘’`]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def evidence_in_abstract(evidence, abstract):
    """Kanıt alıntısı özetin içinde birebir (boşluk/tırnak/kısa çizgi farkları hariç) geçiyor mu?"""
    ev, ab = _norm(evidence).strip(" .,;:"), _norm(abstract)
    return len(ev.split()) >= 6 and ev in ab


def numbers_supported(text, evidence):
    """Türkçe ifadedeki her sayı kanıtta da geçmeli (uydurma sayı/yıl önlemi)."""
    nums = re.findall(r"\d+(?:[.,]\d+)?", text)
    ev = evidence.replace(",", ".")
    return all(n.replace(",", ".") in ev for n in nums)


TR_WORDS = {"ve", "bir", "bu", "için", "ile", "olarak", "da", "de", "ile", "olan", "daha", "gibi", "veya", "ancak",
            "çok", "en", "ise", "sağlar", "kullanılır", "eder", "yapar", "olur", "arasında", "üzerinde", "tarafından"}
EN_WORDS = {"the", "of", "and", "is", "are", "to", "in", "for", "with", "that", "by", "as", "on", "which", "this"}


def is_turkish(text):
    words = re.findall(r"[a-zçğıöşüâîû]+", text.lower())
    if not words or "evidence:" in text.lower():
        return False
    tr = sum(w in TR_WORDS for w in words) + (2 if re.search(r"[çğıöşü]", text.lower()) else 0)
    en = sum(w in EN_WORDS for w in words)
    return tr >= 2 and en <= max(1, len(words) // 8)


def entry_names(meta):
    names = [meta.get("title"), meta.get("title_tr")] + list(meta.get("aliases") or [])
    out = []
    for n in names:
        if n:
            out.append(_norm(re.sub(r"\(.*?\)", "", n)))
    return [n for n in out if n]


def mentions_entry(evidence, names):
    """Kanıt alıntısı bu teknolojinin adından (ya da takma adından) söz ediyor mu? Tekil/çoğul farkı tolere edilir."""
    ev = _norm(evidence)
    ev_t = set(re.findall(r"[a-z0-9]+", ev))
    for n in names:
        toks = [t.rstrip("s") for t in re.findall(r"[a-z0-9]+", n) if t not in ("of", "and", "the", "for", "in")]
        if toks and all(any(e.startswith(t) for e in ev_t) for t in toks):
            return True
    return False


def text_mode(llm=None):
    """'quote': bölümlere yalnızca doğrulanmış kaynak alıntıları yazılır (küçük yerel modellerin Türkçe yeniden
    ifadesi pilotta güvenilir bulunmadı); 'summary': Türkçe özet + görünür alıntı."""
    import os
    m = os.environ.get("KB_LLM_TEXT_MODE")
    if m in ("quote", "summary"):
        return m
    return "quote" if (llm is not None and getattr(llm, "provider", None) == "local") else "summary"


# "(Journal Name, 3, 1994, 294)", "et al." gibi künye parçaları: ad bir dergi adında geçiyor olabilir
CITATION_RE = re.compile(r"\bet al\.|\b(19|20)\d{2}\s*[,;)]\s*\d|\d+\s*,\s*(19|20)\d{2}\b")


GENERIC_TAIL = {"system", "model", "method", "technology", "technique", "proce", "device", "network", "approach"}


def source_focus_ok(source, names):
    """Kaynak gerçekten bu teknoloji hakkında mı? Adı kaynak başlığında geçmeli ya da özette en az iki kez geçmeli.
    (Bir kelimenin geçmesi, kaynağın o teknolojiyi açıkladığı anlamına gelmez.)"""
    if mentions_entry(source.get("title") or "", names):
        return True
    ab = _norm(source.get("abstract"))
    hits = 0
    for n in names:
        toks = [t.rstrip("s") for t in re.findall(r"[a-z0-9]+", n) if t not in ("of", "and", "the", "for", "in")]
        # sondaki genel sözcükler (systems, models, methods...) sayımda zorunlu değil: "CRISPR-Cas tools" da sayılır
        while len(toks) > 1 and toks[-1] in GENERIC_TAIL:
            toks = toks[:-1]
        if toks:
            hits = max(hits, len(re.findall(r"\b" + r"\w*\W+".join(re.escape(t) for t in toks), ab)))
    return hits >= 2


def broad_source_ok(source, names):
    """Disiplin/alt disiplin (derinlik 1–2) için kaynak: başlığında alanın adı geçen bir derleme olmalı."""
    return source.get("type") == "review" and mentions_entry(source.get("title") or "", names)


def validate(draft, sources, names=None, require_turkish=True):
    """Kaynaksız, bilinmeyen kaynaklı, kanıt alıntısı özette bulunmayan ya da kanıtta olmayan sayı içeren
    ifadeleri atar. (temiz taslak, atılanlar)"""
    by = {s["sid"]: s for s in sources}
    preprint = {s["sid"] for s in sources if s.get("peer_reviewed") is False}
    clean, dropped = {}, []
    for key in [f"s{n}" for n in FILL_SECTIONS] + ["conflicts"]:
        out = []
        for st in draft.get(key) or []:
            text = (st.get("text") or "").strip()
            ev = (st.get("evidence") or "").strip()
            srcs = [x for x in st.get("sources") or [] if x in by]
            why = None
            # alıntı modunda model metni kullanılmaz; uzunluk/URL kontrolü yalnızca özet modunda
            if not srcs or (require_turkish and (len(text) < 15 or len(text) > 700 or re.search(r"https?://", text))):
                why = "kaynaksız/geçersiz"
            elif not any(evidence_in_abstract(ev, by[x].get("abstract")) for x in srcs):
                why = "kanıt alıntısı kaynak özetinde yok"
            elif len(ev.split()) > 45:
                why = "kanıt alıntısı çok uzun"
            elif not numbers_supported(text, ev):
                why = "kanıtta olmayan sayı"
            elif require_turkish and not is_turkish(text):
                why = "ifade Türkçe değil / biçim sızıntısı"
            elif names and not mentions_entry(ev, names):
                why = "kanıt bu teknolojiden söz etmiyor"
            elif names and not any(source_focus_ok(by[x], names) for x in srcs):
                why = "kaynak bu teknolojiyi açıklamıyor (yalnızca anıyor)"
            elif CITATION_RE.search(ev):
                why = "alıntı kaynak künyesi içeriyor"
            elif any(_norm(text) == _norm(o["text"]) or _norm(ev) == _norm(o["evidence"])
                     for o in [o for k2 in clean for o in clean[k2]] + out):
                why = "tekrar"
            if why:
                dropped.append({"section": key, "statement": st, "why": why})
                continue
            # dayanak türü modelden değil kaynakların gerçek yayın türünden belirlenir
            basis = "preprint" if set(srcs) <= preprint else (
                "review" if any(by[x].get("type") == "review" for x in srcs) else "peer_reviewed")
            out.append({"text": text, "sources": srcs, "basis": basis, "evidence": ev})
        clean[key] = out
    return clean, dropped


AUTO_NOTE = ("\n\n<sub>Türkçe satırlar alıntılanan kaynak cümlesinin otomatik özetidir (yerel dil modeli); "
             "anlam farkı olursa alıntı esastır. İnsan onayı yok.</sub>")


QUOTE_NOTE = ("\n\n<sub>Bu bölümde yalnızca kaynaklardan birebir alıntılar vardır (yerel dil modeli seçti, "
              "doğrulayıcı kaynak özetinde geçtiğini denetledi). Türkçe özet bekliyor; insan onayı yok.</sub>")


def render(clean, sources, mode="summary"):
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
        if items and mode == "quote":
            out[n] = "\n".join(f"- “{st['evidence']}” " + "".join(f"[{num[s]}]" for s in st["sources"])
                               + (" *(ön baskı)*" if st["basis"] == "preprint" else "") for st in items) + QUOTE_NOTE
        elif items:
            # Kaynak alıntısı esastır ve görünürdür; Türkçe satır otomatik özettir (bkz. bölüm sonu notu)
            out[n] = "\n".join(f"- {st['text']}" + (" *(ön baskı bulgusu)*" if st["basis"] == "preprint" else "")
                               + " " + "".join(f"[{num[s]}]" for s in st["sources"])
                               + (f"\n  > “{st['evidence']}”" if st.get("evidence") else "")
                               for st in items) + AUTO_NOTE
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
    nodes = [n for n in tree.nodes.values() if n["depth"] >= PROPOSAL_DEPTH and
             (refresh or (n["meta"].get("content_status") or "empty") in ("empty", "scope_note"))]
    nodes = [n for n in nodes if not n["meta"].get("maintain_skip_until") or
             n["meta"]["maintain_skip_until"] <= date.today().isoformat()]
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


def apply_draft(cfg, tree, nid, clean, sources, mode="summary"):
    """Boş bölümleri doldurur, dolu bölümler için öneri yazar. (doldurulan bölümler, öneri yolu)"""
    sections, refs = render(clean, sources, mode)
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
        meta["content_status"] = "ai_draft_sourced"   # otomatik içerik daima taslak; doğrulama yalnızca insan
        meta["content_mode"] = "quotes" if mode == "quote" else "summary"
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


AUTO_MIN_DEPTH = 3   # derinlik ≥3: otomatik taslak yazılabilir
PROPOSAL_DEPTH = 2   # derinlik 2: yalnızca öneri; derinlik 1: otomatik içerik üretimi kapalı


def fill_node(cfg, tree, nid, llm=None, http=None, openalex=None, draft=None, sources=None, keep_dropped=False,
              mode=None, exclude=()):
    depth = tree.nodes[nid]["depth"]
    if depth < PROPOSAL_DEPTH:
        return {"node": nid, "status": "disabled_depth1"}
    if sources is None:
        sources = gather_sources(http, cfg, tree, nid, openalex)
        if depth <= 2:  # geniş alan adı ilgisiz çalışmaları getirir; yalnızca alan derlemeleri
            names = entry_names(tree.nodes[nid]["meta"])
            sources = [s for s in sources if broad_source_ok(s, names)]
            for i, s in enumerate(sources):
                s["sid"] = f"S{i + 1}"
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
        draft = llm.json_call("index_draft", DRAFT_SYSTEM, user, DRAFT_SCHEMA, max_tokens=6000, effort="medium")
    mode = mode or text_mode(llm)
    clean, dropped = validate(draft, sources, entry_names(tree.nodes[nid]["meta"]), require_turkish=(mode == "summary"))
    if exclude:  # insan/denetim kararıyla çıkarılan alıntılar
        for k in clean:
            keep = [st for st in clean[k] if not any(x in st["evidence"] for x in exclude)]
            dropped += [{"section": k, "statement": st, "why": "denetimde çıkarıldı"} for st in clean[k] if st not in keep]
            clean[k] = keep
    if depth < AUTO_MIN_DEPTH:  # alt disiplin: _index.md'ye yazılmaz, yalnızca öneri
        sections, refs = render(clean, sources, mode)
        proposal = write_proposal(cfg, nid, "draft", sections, refs,
                                  "Alt disiplin düzeyi (derinlik 2): otomatik yazma kapalı; insan incelemesi için taslak.") \
            if sections else None
        kept = sum(len(v) for v in clean.values())
        return {"node": nid, "status": "proposed" if proposal else "nothing_filled", "filled": [], "kept": kept,
                "mode": mode, "dropped": len(dropped), "sources": len(sources), "proposal": proposal,
                "drop_reasons": {w: sum(1 for d in dropped if d["why"] == w) for w in {d["why"] for d in dropped}}}
    filled, proposal = apply_draft(cfg, tree, nid, clean, sources, mode)
    kept = sum(len(v) for v in clean.values())
    res = {"node": nid, "status": "filled" if filled else "nothing_filled", "filled": filled, "kept": kept, "mode": mode,
           "dropped": len(dropped), "sources": len(sources), "proposal": proposal,
           "drop_reasons": {w: sum(1 for d in dropped if d["why"] == w) for w in {d["why"] for d in dropped}}}
    if keep_dropped:  # denetim raporu için (repoya yazılmaz)
        res["dropped_items"] = dropped
        res["draft"] = draft
        res["source_list"] = sources
    return res


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
