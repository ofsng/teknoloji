---
research_id: doi:10.51583/ijltemas.2026.151000096
title: "Efficient Decoder-Only Transformer with Domain-Specific Byte Pair Encoding for Python Code Generation"
authors: ["P. Venkateshwarlu", "M. Srinivas", "Ravikumar Thallapalli"]
year: 2026
published_date: 2026-11-10
updated_date: 2026-11-18
doi: 10.51583/ijltemas.2026.151000096
arxiv:
url: https://doi.org/10.51583/ijltemas.2026.151000096
publication: "International Journal of Latest Technology in Engineering Management & Applied Science"
publication_type: article
peer_reviewed: true
primary_technology: decoder-only-transformers
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["Python code generation", "decoder-only transformer", "byte pair encoding", "small language models", "perplexity", "GPU memory efficiency", "training time reduction"]
source_ids: ["openalex:W7231961822"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-20
last_checked_at: 2026-11-20
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-20
---

# Efficient Decoder-Only Transformer with Domain-Specific Byte Pair Encoding for Python Code Generation

## 1. Araştırmanın özeti

> Efficient code generation requires a balance between model quality and computational cost, particularly when experiments are performed on resource-constrained hardware. This work investigates the effect of domain-specific Byte Pair Encoding (BPE) on a compact decoder-only Transformer for Python code generation. An 8,000-token Python-specific BPE tokenizer is compared with the 50,258-token GPT-2 tokenizer using the same compact architecture, consisting of two Transformer layers, four attention heads, a model dimension of 128, a feed-forward dimension of 512, and a maximum sequence length of 256 tokens. Experiments use 15,000 training functions, 2,000 validation functions, and 3,000 independent test functions selected with repository-level separation and cross-split duplicate-code verification. On the independent test set, the Python-specific tokenizer reduces average tokenization length by 41.94% and training blocks by 33.89%. The resulting model contains 81.37% fewer parameters, requires 93.79% less training time, and uses 72.40% less peak GPU memory during test evaluation than the GPT-2-tokenizer configuration. However, these efficiency gains are accompanied by lower language-model and code-generation performance. The Custom-BPE model obtains a test perplexity of 125.14, compared with 15.68 for the GPT-2 configuration. These perplexity values are measured over their respective token distributions and are therefore not directly comparable across vocabularies. Under controlled deterministic generation, the Custom-BPE and GPT-2 models produce syntactically valid and compilable outputs in 0% and 26% of cases, respectively. The results therefore characterize an explicit efficiency-versus-generation-quality trade-off rather than a universal quality advantage for domain-specific tokenization.

*Özet kaynağı: openalex:W7231961822 — lisans: cc-by. Tam metin incelenmedi.*

## 2. Ele aldığı problem

_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._

## 3. Kullanılan yöntem

_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._

## 4. Temel bulgular

_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._

## 5. Teknik katkıları

_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._

## 6. Sınırlılıklar

_Tam metin incelenmedi; bu bölüm yalnızca doğrulanabilir kaynakla doldurulabilir._

## 7. İlişkili teknolojiler

<!-- AUTO:TECH:BEGIN (otomatik; elle düzenlemeyin) -->
- **Kanonik konum:** [Yalnız Kod Çözücülü Transformer'lar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.51583/ijltemas.2026.151000096
- OpenAlex: https://openalex.org/W7231961822
- Metadata kaynakları: openalex:W7231961822 (toplama: 2026-11-20)
