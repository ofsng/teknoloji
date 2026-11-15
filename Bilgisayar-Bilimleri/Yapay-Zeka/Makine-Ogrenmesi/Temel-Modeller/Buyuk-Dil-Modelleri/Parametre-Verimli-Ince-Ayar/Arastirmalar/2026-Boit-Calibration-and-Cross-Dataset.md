---
research_id: doi:10.3390/diagnostics16223749
title: "Calibration and Cross-Dataset Behavior in Malaria Microscopy with Parameter-Efficient Fine-Tuning: A Matched LoRA–PiSSA Evaluation"
authors: ["Sorio Boit", "Rajvardhan Patil", "Tiehang Duan"]
year: 2026
published_date: 2026-11-12
updated_date: 2026-11-14
doi: 10.3390/diagnostics16223749
arxiv:
url: https://doi.org/10.3390/diagnostics16223749
publication: Diagnostics
publication_type: article
peer_reviewed: true
primary_technology: parameter-efficient-fine-tuning
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["malaria microscopy", "parameter-efficient fine-tuning", "low-rank adaptation", "LoRa", "vision transformer", "calibration", "cross-dataset generalization", "Plasmodium vivax", "Brier score", "expected calibration error"]
source_ids: ["openalex:W7225905666"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-15
last_checked_at: 2026-11-15
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-15
---

# Calibration and Cross-Dataset Behavior in Malaria Microscopy with Parameter-Efficient Fine-Tuning: A Matched LoRA–PiSSA Evaluation

## 1. Araştırmanın özeti

> Background/Objectives: Reliable evaluation of deep-learning methods for malaria microscopy requires assessing both classification performance and the quality of predicted infection probabilities across datasets. We compared low-rank adaptation (LoRA) and principal singular values and singular vectors adaptation (PiSSA) under matched parameter-efficient fine-tuning (PEFT). Methods: An ImageNet-pretrained vision transformer (ViT-B/16) was adapted at ranks 2, 4, 8, and 16 using 27,558 National Institutes of Health (NIH) malaria cell images. One NIH grouped partition was held fixed across paired training seeds 42, 123, and 456. Models were evaluated on the NIH test split and, without target-domain adaptation, on BBBC041 P. vivax cell crops. The analysis was also replicated in invasive ductal carcinoma (IDC) histopathology. External probability and threshold-transfer analyses were post hoc. Results: Across LoRA and PiSSA configurations, NIH area under the receiver operating characteristic curve (ROC–AUC) ranged from 0.9960 to 0.9970. PiSSA had lower rank-level mean Brier scores and expected calibration error (ECE) at every evaluated rank in NIH and IDC, although paired-run differences varied. On BBBC041, PiSSA-r16 achieved the highest PEFT ROC–AUC (0.8451) and area under the precision–recall curve (PR–AUC, 0.1588), while fully trained reference models performed better. Across all 12 matched external comparisons, PiSSA had lower overall Brier scores and ECE but higher infected-cell Brier scores. PiSSA had lower sensitivity at NIH-derived thresholds in 11 of 12 comparisons. All PEFT models overpredicted infection relative to the observed 2.70% prevalence. Conclusions: Nearly identical internal discrimination concealed differences in external probability behavior and class-specific errors. PiSSA reduced overprediction, but neither adapter achieved adequate external calibration.

*Özet kaynağı: openalex:W7225905666 — lisans: cc-by. Tam metin incelenmedi.*

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

- DOI: https://doi.org/10.3390/diagnostics16223749
- OpenAlex: https://openalex.org/W7225905666
- Metadata kaynakları: openalex:W7225905666 (toplama: 2026-11-15)
