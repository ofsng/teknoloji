"""arXiv API (https://info.arxiv.org/help/api/). Metadata CC0; 3 saniyede en fazla 1 istek, tek bağlantı."""
import re
import xml.etree.ElementTree as ET

from ..records import new_record

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom",
      "os": "http://a9.com/-/spec/opensearch/1.1/"}
# Taksonomi kapsamındaki arXiv arşivleri (ekonomi ve finans kapsam dışı)
CATEGORIES = ["cs.*", "math.*", "stat.*", "eess.*", "q-bio.*", "physics.*", "quant-ph", "cond-mat.*",
              "astro-ph.*", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th", "nucl-ex", "nucl-th", "nlin.*",
              "math-ph"]


def day_query(day):
    d = day.strftime("%Y%m%d")
    cats = " OR ".join(f"cat:{c}" for c in CATEGORIES)
    return f"submittedDate:[{d}0000 TO {d}2359] AND ({cats})"


def fetch_page(http, query, start, size):
    resp = http.get(API, {"search_query": query, "start": start, "max_results": size,
                          "sortBy": "submittedDate", "sortOrder": "ascending"})
    if resp.status != 200:
        raise ValueError(f"arXiv HTTP {resp.status}")
    return parse_feed(resp.body)


def fetch_ids(http, ids):
    resp = http.get(API, {"id_list": ",".join(ids), "max_results": len(ids)})
    if resp.status != 200:
        raise ValueError(f"arXiv HTTP {resp.status}")
    return parse_feed(resp.body)[0]


def _text(el, path):
    x = el.find(path, NS)
    return re.sub(r"\s+", " ", x.text).strip() if x is not None and x.text else None


def parse_feed(body):
    root = ET.fromstring(body)
    total = int(root.findtext("os:totalResults", "0", NS))
    out = []
    for e in root.findall("a:entry", NS):
        raw_id = _text(e, "a:id") or ""
        m = re.search(r"arxiv\.org/abs/(.+)$", raw_id)
        if not m:
            continue  # hata girdisi
        ax = m.group(1)
        base = re.sub(r"v\d+$", "", ax)
        prim = e.find("arxiv:primary_category", NS)
        cats = [c.get("term") for c in e.findall("a:category", NS) if c.get("term")]
        if prim is not None and prim.get("term") in cats:
            cats.remove(prim.get("term"))
            cats.insert(0, prim.get("term"))
        doi = _text(e, "arxiv:doi")
        jref = _text(e, "arxiv:journal_ref")
        rv = []
        if doi or jref:
            rv.append({"relation": "published_version", **({"doi": doi.lower()} if doi else {}),
                       **({"journal_ref": jref} if jref else {}), "source": "arxiv"})
        out.append(new_record(
            title=_text(e, "a:title"),
            authors=[_text(a, "a:name") for a in e.findall("a:author", NS) if _text(a, "a:name")],
            published_date=(_text(e, "a:published") or "")[:10] or None,
            updated_date=(_text(e, "a:updated") or "")[:10] or None,
            doi=doi, arxiv=ax, url=f"https://arxiv.org/abs/{base}",
            publication=jref or "arXiv", publication_type="preprint",
            peer_reviewed=None if (doi or jref) else False,
            abstract=_text(e, "a:summary"), abstract_license="cc0-1.0 (arxiv metadata)",
            source_ids=[f"arxiv:{base.lower()}"],
            categories=[f"arXiv:{c}" for c in cats], related_versions=rv, language="en"))
    return out, total
