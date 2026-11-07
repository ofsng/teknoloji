"""İsteğe bağlı LLM katmanı. Sağlayıcı KB_LLM_PROVIDER ile seçilir:

- `local`     : runner üzerinde çalışan llama.cpp sunucusu (OpenAI uyumlu uç, ücretsiz, anahtarsız).
                Varsayılan model Qwen3-4B-Instruct-2507 (Apache-2.0). Bkz. AUTOMATION.md.
- `openai`    : herhangi bir OpenAI uyumlu uç (ör. Gemini ya da Groq ücretsiz katmanı) — KB_LLM_BASE_URL,
                KB_LLM_API_KEY, KB_LLM_MODEL.
- `anthropic` : Claude API (resmi `anthropic` SDK'sı; ücretli). ANTHROPIC_API_KEY varsa varsayılan.
- (yok)       : sistem LLM'siz, deterministik çalışır.

Aynı istem iki kez modele gönderilmez (state/llm-cache.jsonl); günlük çağrı ve dolar bütçesi aşılınca
BudgetExceeded yükselir ve iş sonraki çalışmaya kalır.
"""
import hashlib
import json
import os
import urllib.error
import urllib.request

# $/1M token (girdi, çıktı) — maliyet tahmini için
PRICES = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-haiku-5-5": (0.10, 0.50),
          "claude-fable-5-1": (10.0, 50.0)}
# Sunucu tarafı geri dönüş (refusal fallback) bu modellerde desteklenir
FALLBACK_MODELS = {"claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1"}


class LLMUnavailable(Exception):
    pass


class BudgetExceeded(Exception):
    pass


class LLMError(Exception):
    pass


def provider_from_env():
    p = os.environ.get("KB_LLM_PROVIDER")
    if p:
        return p
    return "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else None


class OpenAICompatClient:
    """OpenAI uyumlu /chat/completions ucu (llama.cpp sunucusu, Gemini/Groq uyumluluk uçları).
    Yapılandırılmış çıktı response_format.json_schema ile istenir; llama.cpp bunu dilbilgisine çevirir."""

    def __init__(self, base_url, api_key=None, timeout=1800):
        self.base_url, self.api_key, self.timeout = base_url.rstrip("/"), api_key, timeout

    def chat_json(self, model, system, user, schema, max_tokens, name):
        body = {"model": model, "temperature": 0.2, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "response_format": {"type": "json_schema",
                                    "json_schema": {"name": name, "strict": True, "schema": schema}}}
        req = urllib.request.Request(self.base_url + "/chat/completions", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json",
                                              **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {})})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                data = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raise LLMError(f"HTTP {e.code}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            raise LLMUnavailable(f"LLM ucuna erişilemiyor: {e}")
        ch = data["choices"][0]
        if ch.get("finish_reason") == "length":
            raise LLMError("yanıt max_tokens sınırında kesildi")
        usage = data.get("usage") or {}
        return json.loads(ch["message"]["content"]), usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)


class LLM:
    def __init__(self, cfg, counter, client=None, provider=None):
        self.cfg, self.counter = cfg, counter
        self.provider = provider or (None if client else provider_from_env())
        self.compat = None
        self.cache_path = os.path.join(cfg.state_dir, "llm-cache.jsonl")
        self.cache = {}
        if os.path.exists(self.cache_path):
            with open(self.cache_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        e = json.loads(line)
                        self.cache[e["key"]] = e["out"]
                    except (ValueError, KeyError):
                        continue
        self.client = client
        if self.provider == "local":
            self.compat = OpenAICompatClient(os.environ.get("KB_LLM_BASE_URL", "http://127.0.0.1:8080/v1"))
            self.model = os.environ.get("KB_LLM_MODEL", "qwen3-4b-instruct-2507")
        elif self.provider == "openai":
            self.compat = OpenAICompatClient(os.environ["KB_LLM_BASE_URL"], os.environ.get("KB_LLM_API_KEY"))
            self.model = os.environ["KB_LLM_MODEL"]
        else:
            self.model = cfg.llm_model
            if self.client is None and self.provider == "anthropic" and os.environ.get("ANTHROPIC_API_KEY"):
                try:
                    import anthropic
                    self.client = anthropic.Anthropic(max_retries=3, timeout=300.0)
                except ImportError:
                    self.client = None

    @property
    def available(self):
        return self.client is not None or self.compat is not None

    @property
    def trusted_for_classification(self):
        """Küçük yerel modellerin sınıflandırma kararıyla arşive kayıt yazılmaz (yalnızca öneri)."""
        return self.provider not in ("local",) or os.environ.get("KB_LLM_CLASSIFY") == "1"

    def json_call(self, purpose, system, user, schema, max_tokens=8000, effort="low"):
        key = hashlib.sha256(json.dumps([self.provider or "anthropic", self.model, purpose, system, user, schema],
                                        sort_keys=True).encode()).hexdigest()
        if key in self.cache:
            return self.cache[key]
        if not self.available:
            raise LLMUnavailable("ANTHROPIC_API_KEY yok ya da anthropic paketi kurulu değil")
        if self.counter["llm_calls"] >= self.cfg.llm_max_calls or self.counter["llm_usd"] >= self.cfg.llm_max_usd:
            raise BudgetExceeded(f"LLM günlük bütçesi doldu ({self.counter['llm_calls']} çağrı, "
                                 f"${self.counter['llm_usd']:.3f})")
        if self.compat is not None:
            out, tin, tout = self.compat.chat_json(self.model, system, user, schema, max_tokens, purpose)
            self.counter["llm_calls"] += 1
            pin, pout = (0.0, 0.0) if self.provider == "local" else (
                float(os.environ.get("KB_LLM_PRICE_IN", 0)), float(os.environ.get("KB_LLM_PRICE_OUT", 0)))
            self.counter["llm_usd"] = round(self.counter["llm_usd"] + tin * pin / 1e6 + tout * pout / 1e6, 6)
            self._store(key, purpose, out)
            return out
        params = dict(model=self.model, max_tokens=max_tokens, system=system,
                      messages=[{"role": "user", "content": user}],
                      output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}})
        if self.model in FALLBACK_MODELS:
            resp = self.client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default",
                                                    **params)
        else:
            resp = self.client.messages.create(**params)
        self.counter["llm_calls"] += 1
        u = getattr(resp, "usage", None)
        pin, pout = PRICES.get(self.model, (4.0, 20.0))
        if u is not None:
            self.counter["llm_usd"] = round(self.counter["llm_usd"] + (getattr(u, "input_tokens", 0) or 0) * pin / 1e6
                                            + (getattr(u, "output_tokens", 0) or 0) * pout / 1e6, 6)
        if resp.stop_reason == "refusal":
            raise LLMError("model isteği reddetti")
        if resp.stop_reason == "max_tokens":
            raise LLMError("yanıt max_tokens sınırında kesildi")
        text = next((b.text for b in resp.content if getattr(b, "type", None) == "text"), None)
        if text is None:
            raise LLMError("yanıtta metin bloğu yok")
        out = json.loads(text)
        self._store(key, purpose, out)
        return out

    def _store(self, key, purpose, out):
        self.cache[key] = out
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "purpose": purpose, "provider": self.provider, "model": self.model,
                                "out": out}, ensure_ascii=False) + "\n")
