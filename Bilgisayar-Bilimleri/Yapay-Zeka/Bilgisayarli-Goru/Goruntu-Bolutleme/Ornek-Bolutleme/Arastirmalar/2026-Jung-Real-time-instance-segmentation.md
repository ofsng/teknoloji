---
research_id: doi:10.1371/journal.pone.0361612
title: "Real-time instance segmentation of spine endoscopy images using a YOLO-V11 deep convolutional neural network"
authors: ["Hyun Ji Jung", "Noah Euyhyun Nam", "Chulmin Lee", "Y. K. KIM C. S. LIM", "Wonchang Choi", "Junsu Lee", "Gunyul Kim", "Hyunjae Kim", "Sang Kyeong Lee", "Jiho Kang", "Taeshin Kim"]
year: 2026
published_date: 2026-11-18
updated_date: 2026-11-21
doi: 10.1371/journal.pone.0361612
arxiv:
url: https://doi.org/10.1371/journal.pone.0361612
publication: "PLoS ONE"
publication_type: article
peer_reviewed: true
primary_technology: instance-segmentation
related_technologies: ["convolutional-neural-networks", "single-stage-detectors"]
classification_confidence: high
classification_method: deterministic
keywords: ["instance segmentation", "real-time segmentation", "surgical instrument detection", "bleeding detection", "ligamentum flavum", "dura mater", "radiofrequency ablation", "surgical guidance", "robotic spine surgery", "multi-class object detection"]
source_ids: ["openalex:W7235897871"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-21
last_checked_at: 2026-11-21
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-21
---

# Real-time instance segmentation of spine endoscopy images using a YOLO-V11 deep convolutional neural network

## 1. Araştırmanın özeti

> BACKGROUND AND OBJECTIVES: Spine endoscopic surgery requires precise anatomical recognition and real-time bleeding detection to enhance surgical safety and efficiency. However, most existing computer vision studies do not offer real-time multi-class segmentation of the entire scene. This study aims to develop a real-time instance segmentation model based on YOLO-V11, capable of automatically identifying surgical instruments, critical anatomical structures, and bleeding sites in spine endoscopy. METHODS: The model was trained and evaluated using 2,181 annotated frames (training 1,741 / validation 216 / held-out test 224) from spine endoscopy images, covering nine key categories: instruments, bone, ligamentum flavum, dura, soft tissue, vessels, fat, the radiofrequency ablation wand, and bleeding focus. The segmentation model's performance was evaluated across various YOLO-V11 variants. RESULTS: Across five random seeds per variant on the same NVIDIA A100 GPU, YOLO-V11 l achieved the highest mask mAP50, defined as mean average precision at an intersection-over-union threshold of 0.50, with a value of 0.7735 ± 0.0030 (mean ± SD, n = 5). It also maintained real-time inference, reaching 270 ± 35 frames per second (FPS) with a per-frame latency of 3.75 ± 0.51 ms. All five variants exceeded 30 FPS, the widely accepted real-time threshold for surgical imaging. The model demonstrated high precision in segmenting vital structures such as the dura and ligamentum flavum and accurately identified bleeding regions. CONCLUSION: This research contributes to AI-driven surgical guidance systems, with potential applications in robotic-assisted spine surgery. The developed model enables real-time navigation, improving intraoperative decision-making and enhancing surgical outcomes. In particular, our YOLO-V11-based framework extends prior single-structure or lower-frame-rate multi-element approaches by delivering real-time multi-class instance segmentation of instruments, anatomical structures, and bleeding sites in spine endoscopy, with explicitly quantified inference latency.

*Özet kaynağı: openalex:W7235897871 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Örnek Bölütleme](../_index.md)
- **İlişkili:** [Evrişimli Sinir Ağları](../../../../Makine-Ogrenmesi/Derin-Ogrenme/Evrisimli-Sinir-Aglari/_index.md), [Tek Aşamalı Dedektörler](../../../Nesne-Tespiti/Tek-Asamali-Dedektorler/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1371/journal.pone.0361612
- OpenAlex: https://openalex.org/W7235897871
- Metadata kaynakları: openalex:W7235897871 (toplama: 2026-11-21)
