"""Kaynaktan bağımsız araştırma kaydı ve aynı çalışmanın farklı kayıtlarının birleştirilmesi.

Kayıt alanları yalnızca kaynağın verdiği bilgilerden doldurulur; eksik alan boş bırakılır.
"""
import kb

# Özetin depoya kopyalanabileceği lisanslar (depo herkese açık). arXiv metadata'sı CC0'dır.
PERMISSIVE_LICENSES = {"cc0", "cc-by", "cc-by-sa", "public-domain", "pd", "cc0-1.0 (arxiv metadata)"}


def new_record(**kw):
    r = {"title": None, "authors": [], "published_date": None, "updated_date": None, "doi": None, "arxiv": None,
         "url": None, "publication": None, "publication_type": None, "peer_reviewed": None, "abstract": None,
         "abstract_license": None, "source_ids": [], "categories": [], "topics": [], "keywords": [],
         "cited_by_count": None, "is_retracted": None, "related_versions": [], "language": None}
    r.update(kw)
    r["doi"] = kb.norm_doi(r.get("doi"))
    if r["doi"] and r["doi"].startswith("10.48550/arxiv."):
        r["arxiv"] = r["arxiv"] or r["doi"][len("10.48550/arxiv."):]
        r["doi"] = None
    r["arxiv"] = kb.norm_arxiv(r.get("arxiv"))
    return r


def year_of(r):
    pd = r.get("published_date") or ""
    return int(pd[:4]) if pd[:4].isdigit() else None


def keys(r):
    return kb.research_keys({"doi": r.get("doi"), "arxiv": r.get("arxiv"), "title": r.get("title"),
                             "year": year_of(r)})


def strong_keys(r):
    """Başlık anahtarı hariç (DOI / arXiv); kaynaklar arası birleştirmede kullanılır."""
    return {k for k in keys(r) if not k.startswith("title:")}


def abstract_allowed(r):
    lic = (r.get("abstract_license") or "").lower()
    return bool(r.get("abstract")) and lic in PERMISSIVE_LICENSES


def merge(a, b):
    """Aynı çalışmaya ait iki kaydı birleştir. Hakemli (yayımlanmış) sürümün yayın bilgisi tercih edilir;
    ön baskı ilişkisi related_versions alanında korunur."""
    pub, other = (b, a) if (b.get("peer_reviewed") is True and a.get("peer_reviewed") is not True) else (a, b)
    out = dict(pub)
    for f in ("title", "doi", "arxiv", "url", "publication", "publication_type", "published_date",
              "updated_date", "language"):
        out[f] = pub.get(f) or other.get(f)
    if not out.get("authors"):
        out["authors"] = other.get("authors") or []
    if not abstract_allowed(out) and abstract_allowed(other):
        out["abstract"], out["abstract_license"] = other["abstract"], other["abstract_license"]
    elif not out.get("abstract"):
        out["abstract"], out["abstract_license"] = other.get("abstract"), other.get("abstract_license")
    for f in ("source_ids", "categories", "topics", "keywords"):
        out[f] = list(dict.fromkeys((pub.get(f) or []) + (other.get(f) or [])))
    out["cited_by_count"] = max((x for x in (a.get("cited_by_count"), b.get("cited_by_count")) if x is not None),
                                default=None)
    out["is_retracted"] = True if (a.get("is_retracted") or b.get("is_retracted")) else (
        a.get("is_retracted") if a.get("is_retracted") is not None else b.get("is_retracted"))
    if pub.get("peer_reviewed") is True or other.get("peer_reviewed") is True:
        out["peer_reviewed"] = True
    rv = (pub.get("related_versions") or []) + (other.get("related_versions") or [])
    if other.get("peer_reviewed") is False and pub.get("peer_reviewed") is True and other.get("arxiv"):
        rv.append({"relation": "preprint", "arxiv": other["arxiv"], "source": "merge"})
    seen, uniq = set(), []
    for v in rv:
        k = tuple(sorted(v.items()))
        if k not in seen:
            seen.add(k)
            uniq.append(v)
    out["related_versions"] = uniq
    return out


def dedupe_batch(records):
    """Bir çalışma içinde (ör. arXiv + OpenAlex) aynı çalışmanın kayıtlarını birleştir."""
    out, index = [], {}
    for r in records:
        hit = next((index[k] for k in strong_keys(r) | {k for k in keys(r) if k.startswith("title:")} if k in index), None)
        if hit is None:
            out.append(r)
            pos = len(out) - 1
        else:
            out[hit] = merge(out[hit], r)
            pos = hit
        for k in keys(out[pos]):
            index[k] = pos
    return out
