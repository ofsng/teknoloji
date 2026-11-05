"""OpenAlex API (https://help.openalex.org). Veri CC0. Anahtarsız: IP başına paylaşılan küçük günlük bütçe;
ücretsiz anahtar (OPENALEX_API_KEY) kendi $1/gün bütçesini verir. Liste çağrısı ~$0.0001, arama ~$0.001.
`from_created_date` ücretli plan gerektirdiğinden günlük toplama yayın tarihine göre yapılır."""
from ..records import new_record

API = "https://api.openalex.org/works"
ARXIV_SOURCE = "S4306400194"  # arXiv kayıtları doğrudan arXiv'den toplanır; burada tekrar çekilmez
SELECT = ("id,doi,title,publication_date,updated_date,type,authorships,primary_location,locations,"
          "primary_topic,keywords,abstract_inverted_index,cited_by_count,is_retracted,language")
BIORXIV, MEDRXIV = "S4306402567", "S3005729997"
# 1 Life Sciences, 3 Physical Sciences, 4 Health Sciences (2 Social Sciences kapsam dışı).
# Kalite: genel depolar (ör. Zenodo) hakemsiz ve denetimsiz içerik barındırdığından günlük akışa alınmaz;
# yalnızca dergi/konferans yayınları ve bioRxiv/medRxiv ön baskıları toplanır.
_BASE = "from_publication_date:{d},to_publication_date:{d},has_abstract:true,primary_topic.domain.id:1|3|4,language:en"
DAILY_STREAMS = {
    "journal": _BASE + ",type:article|review,primary_location.source.type:journal|conference",
    "biorxiv-medrxiv": _BASE + f",primary_location.source.id:{BIORXIV}|{MEDRXIV}",
}


def _params(cfg, extra):
    p = dict(extra)
    p["select"] = SELECT
    if cfg.openalex_key:
        p["api_key"] = cfg.openalex_key
    if cfg.contact_email:
        p["mailto"] = cfg.contact_email
    return p


def _get(http, cfg, params):
    resp = http.get(API, _params(cfg, params))
    if resp.status != 200:
        raise ValueError(f"OpenAlex HTTP {resp.status}: {resp.body[:200]!r}")
    data = resp.json()
    return [to_record(w) for w in data.get("results", [])], data.get("meta", {})


def list_day(http, cfg, day, page, stream="journal"):
    return _get(http, cfg, {"filter": DAILY_STREAMS[stream].format(d=day.isoformat()),
                            "per_page": cfg.openalex_per_page, "page": page})


def search_top(http, cfg, phrase, n, types="article|review", field="title_and_abstract"):
    """Tarihsel tamamlama ve bilgi bakımı için: ifadeyi başlıkta (ya da başlık/özette) geçen en çok atıf alan
    dergi/konferans çalışmaları."""
    q = phrase.replace('"', "")
    return _get(http, cfg, {"filter": f'{field}.search:"{q}",type:{types},has_abstract:true,'
                                      f'primary_location.source.type:journal|conference',
                            "sort": "cited_by_count:desc", "per_page": n})[0]


def count_phrase(http, cfg, phrase):
    q = phrase.replace('"', "")
    resp = http.get(API, _params(cfg, {"filter": f'title_and_abstract.search:"{q}"', "per_page": 1,
                                       "select": "id"}))
    if resp.status != 200:
        raise ValueError(f"OpenAlex HTTP {resp.status}")
    return resp.json().get("meta", {}).get("count", 0)


def abstract_text(inv):
    if not inv:
        return None
    pos = []
    for word, idxs in inv.items():
        for i in idxs:
            pos.append((i, word))
    return " ".join(w for _, w in sorted(pos)) or None


def to_record(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    arxiv = None
    for l in w.get("locations") or []:
        url = (l.get("landing_page_url") or "")
        if "arxiv.org/abs/" in url:
            arxiv = url.split("arxiv.org/abs/")[1]
    typ = w.get("type")
    if typ == "preprint" or src.get("type") == "repository":
        peer = False if typ == "preprint" else None
    elif src.get("type") in ("journal", "conference") and loc.get("version") in ("publishedVersion", None):
        peer = True
    else:
        peer = None
    pt = w.get("primary_topic") or {}
    # alan (field) adı konu metnine katılmaz; sınıflandırıcıda öncül olarak kullanılır
    topics = [x for x in [pt.get("display_name"), (pt.get("subfield") or {}).get("display_name")] if x]
    return new_record(
        title=w.get("title"),
        authors=[(a.get("author") or {}).get("display_name") for a in (w.get("authorships") or [])
                 if (a.get("author") or {}).get("display_name")],
        published_date=w.get("publication_date"), updated_date=(w.get("updated_date") or "")[:10] or None,
        doi=w.get("doi"), arxiv=arxiv, url=w.get("doi") or loc.get("landing_page_url"),
        publication=src.get("display_name"), publication_type=typ, peer_reviewed=peer,
        abstract=abstract_text(w.get("abstract_inverted_index")), abstract_license=loc.get("license"),
        source_ids=[f"openalex:{w.get('id', '').rsplit('/', 1)[-1]}"],
        categories=[f"OpenAlex-field:{(pt.get('field') or {}).get('display_name')}"] if pt.get("field") else [],
        topics=topics, keywords=[k.get("display_name") for k in (w.get("keywords") or []) if k.get("display_name")],
        cited_by_count=w.get("cited_by_count"), is_retracted=w.get("is_retracted"), language=w.get("language"))
