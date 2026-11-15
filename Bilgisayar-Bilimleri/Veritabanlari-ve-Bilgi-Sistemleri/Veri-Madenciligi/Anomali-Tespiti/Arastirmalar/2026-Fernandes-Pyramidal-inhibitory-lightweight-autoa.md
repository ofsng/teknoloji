---
research_id: doi:10.1007/s44163-026-02671-5
title: "Pyramidal inhibitory lightweight autoassociative reconstruction for cost-constrained visual anomaly detection"
authors: ["Bruno Fernandes"]
year: 2026
published_date: 2026-11-09
updated_date: 2026-11-13
doi: 10.1007/s44163-026-02671-5
arxiv:
url: https://doi.org/10.1007/s44163-026-02671-5
publication: "Discover Artificial Intelligence"
publication_type: article
peer_reviewed: true
primary_technology: anomaly-detection
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["image anomaly detection", "reconstruction-based anomaly detection", "lateral inhibition", "lightweight neural networks", "edge computing", "industrial inspection", "MVTec AD", "Visa"]
source_ids: ["openalex:W7225653349"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-14
last_checked_at: 2026-11-14
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-14
---

# Pyramidal inhibitory lightweight autoassociative reconstruction for cost-constrained visual anomaly detection

## 1. Araştırmanın özeti

> Abstract Visual anomaly detection plays an important role in industrial inspection, edge monitoring and visual quality control, particularly where abnormal samples are rare, heterogeneous, and often unavailable during training. Recent deep anomaly detection approaches have achieved high classification performance by leveraging pretrained backbones, memory banks, nearest-neighbor search, synthetic anomaly generation, or auxiliary discriminators. However, these methods often increase parameter count, floating-point operations (FLOPs), memory usage, update size, and energy consumption, which complicates deployment on cost-constrained industrial or edge hardware. This study introduces PILAR (Pyramidal Inhibitory Lightweight Autoassociative Reconstruction), a compact reconstruction-based architecture for anomaly detection. PILAR employs a pyramidal autoassociative encoder-decoder with local receptive fields, a spatial bottleneck, pure-pyramid reconstruction, and lateral inhibition to promote local competition within feature maps. The model is trained only with normal samples, and the anomaly score is obtained from reconstruction residuals. Thus, during inference, PILAR does not require class prototypes, covariance matrices, support vectors, density parameters, nearest-neighbor databases, or discriminator states. PILAR is evaluated on MNIST, Fashion-MNIST, CIFAR-10, MVTec AD, and VisA datasets using direct image reconstruction, whole-image RGB reconstruction, patchwise RGB reconstruction, and Feature-PILAR-FCN, a fully convolutional feature-space variant that uses compact PILAR heads to reconstruct selected frozen feature maps. In the evaluated implementation, these maps are taken from ResNet18 layer 2 and layer 3 prior to residual scoring. The proposed detector reaches $$98.86\pm 0.04\%$$ Image-AP and $$92.63\pm 0.05\%$$ AUPRO@30 on MVTec AD over five seeds; the unchanged industrial configuration reaches $$92.53\pm 0.07\%$$ Image-AUROC on VisA. Compared with the evaluated ResNet18 configurations of SimpleNet and GLASS, Feature-PILAR-FCN retains 35.6% fewer inference parameters and achieves 5.2–5.6 times their throughput at batch size 16 on the same Apple M4 Max GPU in FP32, despite higher single-image latency. These results indicate that PILAR can be used as a low-state anomaly detector when memory footprint and computational cost are relevant constraints. They also show that direct RGB reconstruction is useful mainly in selected low-cost screening cases, while broader industrial detection requires a more informative representation, which in this work is obtained from frozen feature maps.

*Özet kaynağı: openalex:W7225653349 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Anomali Tespiti](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1007/s44163-026-02671-5
- OpenAlex: https://openalex.org/W7225653349
- Metadata kaynakları: openalex:W7225653349 (toplama: 2026-11-14)
