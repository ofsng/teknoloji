"""Crossref REST API: DOI doğrulama, yayın ilişkileri (ön baskı ↔ yayın) ve düzeltme/geri çekme bildirimleri
(Retraction Watch verisi Crossref'e entegredir). Public havuz: 5 istek/aralık, eşzamanlılık 1;
KB_CONTACT_EMAIL verilirse polite havuz (mailto)."""
import urllib.parse

API = "https://api.crossref.org/works"
NOTICE_TYPES = {"retraction", "withdrawal", "removal", "partial_retraction", "correction", "erratum",
                "corrigendum", "expression_of_concern"}
SEVERE = {"retraction", "withdrawal", "removal", "partial_retraction"}
PEER_TYPES = {"journal-article", "proceedings-article", "book-chapter"}


def _params(cfg, p=None):
    p = dict(p or {})
    if cfg.contact_email:
        p["mailto"] = cfg.contact_email
    return p


def lookup(http, cfg, doi):
    """Crossref kaydı (sözlük) ya da kayıt yoksa None. Erişim sorununda SourceUnavailable yükselir."""
    resp = http.get(f"{API}/{urllib.parse.quote(doi, safe='/')}", _params(cfg))
    if resp.status == 404:
        return None
    if resp.status != 200:
        raise ValueError(f"Crossref HTTP {resp.status}")
    m = resp.json()["message"]
    rel = m.get("relation") or {}
    return {
        "type": m.get("type"),
        "publication": (m.get("container-title") or [None])[0],
        "peer_reviewed": True if m.get("type") in PEER_TYPES else (False if m.get("type") == "posted-content" else None),
        "has_preprint": [x.get("id") for x in rel.get("has-preprint", [])],
        "is_preprint_of": [x.get("id") for x in rel.get("is-preprint-of", [])],
        "update_to": m.get("update-to") or [],
    }


def doi_registered(http, doi):
    """Crossref dışı (ör. DataCite) DOI'ler için doi.org tanıtıcı API'siyle varlık kontrolü."""
    resp = http.get(f"https://doi.org/api/handles/{urllib.parse.quote(doi, safe='/')}")
    if resp.status == 404:
        return False
    if resp.status != 200:
        raise ValueError(f"doi.org HTTP {resp.status}")
    return resp.json().get("responseCode") == 1


def notices_for(http, cfg, doi):
    """DOI'yi güncelleyen bildirimler: [{'type','notice_doi','date','source'}]."""
    resp = http.get(API, _params(cfg, {"filter": f"updates:{doi}", "rows": 20, "select": "DOI,update-to"}))
    if resp.status != 200:
        raise ValueError(f"Crossref HTTP {resp.status}")
    out = []
    for item in resp.json()["message"].get("items", []):
        for u in item.get("update-to") or []:
            if (u.get("DOI") or "").lower() == doi.lower() and u.get("type") in NOTICE_TYPES:
                dp = ((u.get("updated") or {}).get("date-parts") or [[None]])[0]
                out.append({"type": u["type"], "notice_doi": item.get("DOI"), "source": u.get("source"),
                            "date": "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(dp) if x)})
    return out
