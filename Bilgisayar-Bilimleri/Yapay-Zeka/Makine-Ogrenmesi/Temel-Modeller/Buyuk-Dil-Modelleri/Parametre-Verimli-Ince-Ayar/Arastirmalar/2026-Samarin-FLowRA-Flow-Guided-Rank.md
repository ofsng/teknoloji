---
research_id: doi:10.3390/make8110389
title: "FLowRA: Flow-Guided Rank Allocation for Parameter-Efficient Fine-Tuning of Deep Neural Networks"
authors: ["Aleksei Samarin", "Artem Nazarenko", "Egor Kotenko", "Aleksei Toropov", "Dmitry Nazarenko", "Julia Afonina", "Aleksandra Dozortseva", "Alexander Savelev", "Elena Mikhailova", "Alexandr A. Motyko", "Valentin Malykh"]
year: 2026
published_date: 2026-11-19
updated_date: 2026-11-21
doi: 10.3390/make8110389
arxiv:
url: https://doi.org/10.3390/make8110389
publication: "Machine Learning and Knowledge Extraction"
publication_type: article
peer_reviewed: true
primary_technology: parameter-efficient-fine-tuning
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["low-rank adaptation", "LoRa", "parameter-efficient fine-tuning", "DORA", "representational change"]
source_ids: ["openalex:W7236675494"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-24
last_checked_at: 2026-11-24
content_verified: false
identifier_verified: crossref
---

# FLowRA: Flow-Guided Rank Allocation for Parameter-Efficient Fine-Tuning of Deep Neural Networks

## 1. Araştırmanın özeti

> Low-rank adaptation (LoRA) is widely used for parameter-efficient fine-tuning, yet uniform rank assignment ignores the varying contribution of layers to a downstream task. Adaptive methods such as AdaLoRA allocate ranks via gradient and singular-value importance, but they do not exploit the representation change induced by the task. We introduce FLowRA, a calibration-based rank-allocation framework that combines a lightweight flow-change descriptor (velocity, acceleration, and directional alignment of hidden representations) with gradient activity to solve a constrained integer-budget problem. FLowRA complements existing LoRA variants, requires only two user-configurable parameters, and supports multiple architectures through architecture-specific implementations. On GLUE, SuperGLUE, instruction-following, code, vision, and vision-language benchmarks, FLowRA consistently outperforms uniform LoRA, DoRA, and AdaLoRA under low trainable-parameter budgets, reducing the gap to full fine-tuning by 48.5% on GLUE relative to the strongest baseline. We compare FLowRA with AdaLoRA using sensitivity-score correlations and report component ablations to assess the contribution of flow-guided allocation.

*Özet kaynağı: openalex:W7236675494 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Parametre Verimli İnce Ayar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/make8110389
- OpenAlex: https://openalex.org/W7236675494
- Metadata kaynakları: openalex:W7236675494 (toplama: 2026-11-24)
