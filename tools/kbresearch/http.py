"""Kota dostu HTTP istemcisi: ana makine başına en küçük istek aralığı, kontrollü yeniden deneme."""
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

# Belgelenmiş sınırlar: arXiv 3 sn'de 1 istek; Crossref public havuz 5 istek/aralık, eşzamanlılık 1;
# OpenAlex anahtarsız 10 istek/sn. Değerler güvenli tarafta tutuldu.
HOST_INTERVAL = {"export.arxiv.org": 3.1, "api.crossref.org": 0.3, "api.openalex.org": 0.15, "doi.org": 0.3}
RETRY_STATUS = {429, 500, 502, 503, 504}


class SourceUnavailable(Exception):
    """Kaynak yeniden denemelere rağmen erişilemez; çağıran işlemi bir sonraki çalışmaya bırakmalı."""


class Response:
    def __init__(self, status, headers, body):
        self.status, self.headers, self.body = status, headers, body

    def json(self):
        return json.loads(self.body.decode("utf-8"))


class Http:
    def __init__(self, user_agent, opener=None, sleep=time.sleep, clock=time.monotonic, max_retries=4, timeout=60):
        self.user_agent = user_agent
        self.opener = opener or self._urlopen
        self.sleep, self.clock = sleep, clock
        self.max_retries, self.timeout = max_retries, timeout
        self.last = {}
        self.calls = {}

    def _urlopen(self, req, timeout):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return Response(r.status, dict(r.headers), r.read())
        except urllib.error.HTTPError as e:
            return Response(e.code, dict(e.headers or {}), e.read() if e.fp else b"")

    def _pace(self, host):
        gap = HOST_INTERVAL.get(host, 0.2)
        wait = self.last.get(host, -1e9) + gap - self.clock()
        if wait > 0:
            self.sleep(wait)
        self.last[host] = self.clock()

    def get(self, url, params=None, headers=None):
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, safe=":,|!*()[]\"")
        host = urllib.parse.urlparse(url).netloc
        hdrs = {"User-Agent": self.user_agent, **(headers or {})}
        delay = 2.0
        for attempt in range(self.max_retries + 1):
            self._pace(host)
            self.calls[host] = self.calls.get(host, 0) + 1
            try:
                resp = self.opener(urllib.request.Request(url, headers=hdrs), self.timeout)
            except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError) as e:
                err = f"{type(e).__name__}: {e}"
                resp = None
            if resp is not None and resp.status not in RETRY_STATUS:
                return resp
            if resp is not None:
                err = f"HTTP {resp.status}"
                ra = (resp.headers or {}).get("Retry-After") or (resp.headers or {}).get("retry-after")
                if ra and str(ra).isdigit():
                    delay = max(delay, min(float(ra), 120.0))
            if attempt < self.max_retries:
                self.sleep(delay)
                delay = min(delay * 2, 120.0)
        raise SourceUnavailable(f"{host}: {err} ({self.max_retries + 1} deneme)")
