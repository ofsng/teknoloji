---
research_id: arxiv:2611.04112
title: "Co-Occurrence Priors Override Visual Spatial Evidence: Understanding False Alarms in Vision-Language Models for Construction Struck-By Hazard Detection"
authors: ["Xiaoshan Zhou"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-03
doi:
arxiv: 2611.04112
url: https://arxiv.org/abs/2611.04112
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: vision-language-models
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.04112"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-05
last_checked_at: 2026-11-05
content_verified: false
identifier_verified: arxiv
---

# Co-Occurrence Priors Override Visual Spatial Evidence: Understanding False Alarms in Vision-Language Models for Construction Struck-By Hazard Detection

## 1. Araştırmanın özeti

> Vision-language models (VLMs) increasingly support construction hazard monitoring, yet their frequent false alarms remain poorly understood. This study investigates whether false struck-by hazard warnings arise from failures in object recognition, spatial relation encoding, or hazard decisions dominated by learned co-occurrence priors. We evaluated Qwen2.5-VL-7B and InternVL3.5-8B using 355 counterfactual worker-excavator scene pairs with controlled spatial proximity and worker-removal variants, combining behavioral analysis, internal representation probing, causal interventions, and decision correction. Both models recognized the entities and encoded their spatial relations (out-of-fold AUROC: 0.82 and 0.91), assigning higher hazard scores to near than far scenes in 79% and 73% of pairs. Nevertheless, 74% and 100% of far scenes were falsely classified as hazardous. Removing the worker reduced Qwen's hazard rate to 11%, while worker presence exerted 2.4- and 3.2-times greater influence on hazard scores than spatial proximity in the respective models. Attention-head interventions, neuron-level interventions, and activation steering failed to eliminate this co-occurrence bias. However, conditioning hazard decisions on the model's own spatial-relation representation improved Qwen's specificity from 0.36 to 0.58 at matched sensitivity, outperforming threshold recalibration. These findings reveal that VLM struck-by false alarms stem primarily from decision-making failures rather than deficiencies in object recognition or spatial encoding, suggesting that future efforts should prioritize conditioning hazard decisions on encoded spatial evidence rather than further improving visual recognition alone.

*Özet kaynağı: arxiv:2611.04112 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Görü-Dil Modelleri](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.04112
- Metadata kaynakları: arxiv:2611.04112 (toplama: 2026-11-05)
