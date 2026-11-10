---
research_id: doi:10.1088/1361-6560/aebf1c
title: "Quantifying multi-lesion detection and localization in whole-body FDG PET/CT with a multimodal foundation model"
authors: ["Xiaofeng Liu", "Menghua Xia", "Yanis Chemli", "Georges El Fakhri", "Chi Liu", "Jinsong Ouyang"]
year: 2026
published_date: 2026-11-06
updated_date: 2026-11-09
doi: 10.1088/1361-6560/aebf1c
arxiv:
url: https://doi.org/10.1088/1361-6560/aebf1c
publication: "Physics in Medicine and Biology"
publication_type: article
peer_reviewed: true
primary_technology: multimodal-foundation-models
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["lesion localization", "multimodal foundation models", "tumor detection", "lesion size"]
source_ids: ["openalex:W7225391804"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-10
last_checked_at: 2026-11-10
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-10
---

# Quantifying multi-lesion detection and localization in whole-body FDG PET/CT with a multimodal foundation model

## 1. Araştırmanın özeti

> ObjectiveTo develop a 3D AI framework for detecting and localizing multiple lesions in whole-body FDG PET/CT, and to evaluate whether a pretrained PET/CT foundation model can improve lesion detection performance compared with conventional training from scratch.ApproachThe AutoPET cohort comprised 1,014 studies divided into 700 training, 114 validation, and 200 subject-independent test studies. Tumor masks were converted into 3D bounding boxes. We developed a one-stage 3D lesion detector using a PlainConvUNet backbone to extract multi-scale encoder-decoder features for lesion classification and box regression. To leverage foundation-model representations, the PlainConvUNet backbone was initialized with weights from our previously developed multi-center PET/CT foundation model, pretrained using masked autoencoding, and subsequently fine-tuned for lesion detection. Four configurations were compared: PET+CT trained from scratch, PET only, CT only, and PET+CT initialized from the pretrained PET/CT foundation model. Detection performance was evaluated using free-response receiver operating characteristic (FROC) and alternative FROC (AFROC) analyses, qualitative analysis, and lesion-size-stratified operating curves.Main resultsMultimodal PET+CT consistently outperformed either modality alone across task-based detection metrics, demonstrating the complementary contributions of metabolic and anatomical information. Importantly, initialization from the pretrained PET/CT foundation model further enhanced lesion detection performance compared with training the same PET+CT detector from scratch, increasing absolute FROC sensitivity by 0.034-0.041 across the evaluated 1-4 false-positive-per-scan operating range and improving AFROC AUC by 0.028. Detection performance increased with lesion size, with small lesions remaining the most challenging. The separation between the pretrained and randomly initialized PET+CT configurations was more evident in the smaller-lesion strata, whereas their operating curves increasingly overlapped for larger lesions.SignificanceThis study provides a detection-centered, task-based characterization of multi-lesion analysis in whole-body PET/CT. Multimodal PET+CT improves lesion detection compared with either modality alone, lesion size is a major determinant of detection performance, and initialization from a pretrained PET/CT foundation model provides an additional performance improvement.

*Özet kaynağı: openalex:W7225391804 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çok Kipli Temel Modeller](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1088/1361-6560/aebf1c
- OpenAlex: https://openalex.org/W7225391804
- Metadata kaynakları: openalex:W7225391804 (toplama: 2026-11-10)
