"""İsteğe bağlı LLM katmanı (Anthropic Claude API, resmi `anthropic` Python SDK'sı).

- Anahtar yoksa ya da `anthropic` kurulu değilse sistem LLM'siz (deterministik) çalışır.
- Aynı istem iki kez modele gönderilmez: yanıtlar state/llm-cache.jsonl içinde önbelleklenir.
- Günlük çağrı ve dolar bütçesi aşılınca BudgetExceeded yükselir; işlem sonraki çalışmaya kalır.
- Model varsayılanı claude-opus-5-5; KB_LLM_MODEL ile değiştirilebilir (doğruluk ölçülerek seçilmeli).
"""
import hashlib
import json
import os

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


class LLM:
    def __init__(self, cfg, counter, client=None):
        self.cfg, self.counter = cfg, counter
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
        if self.client is None and os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self.client = anthropic.Anthropic(max_retries=3, timeout=300.0)
            except ImportError:
                self.client = None

    @property
    def available(self):
        return self.client is not None

    def json_call(self, purpose, system, user, schema, max_tokens=8000, effort="low"):
        key = hashlib.sha256(json.dumps([self.cfg.llm_model, purpose, system, user, schema],
                                        sort_keys=True).encode()).hexdigest()
        if key in self.cache:
            return self.cache[key]
        if not self.available:
            raise LLMUnavailable("ANTHROPIC_API_KEY yok ya da anthropic paketi kurulu değil")
        if self.counter["llm_calls"] >= self.cfg.llm_max_calls or self.counter["llm_usd"] >= self.cfg.llm_max_usd:
            raise BudgetExceeded(f"LLM günlük bütçesi doldu ({self.counter['llm_calls']} çağrı, "
                                 f"${self.counter['llm_usd']:.3f})")
        params = dict(model=self.cfg.llm_model, max_tokens=max_tokens, system=system,
                      messages=[{"role": "user", "content": user}],
                      output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}})
        if self.cfg.llm_model in FALLBACK_MODELS:
            resp = self.client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default",
                                                    **params)
        else:
            resp = self.client.messages.create(**params)
        self.counter["llm_calls"] += 1
        u = getattr(resp, "usage", None)
        pin, pout = PRICES.get(self.cfg.llm_model, (4.0, 20.0))
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
        self.cache[key] = out
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "purpose": purpose, "model": self.cfg.llm_model, "out": out},
                               ensure_ascii=False) + "\n")
        return out
