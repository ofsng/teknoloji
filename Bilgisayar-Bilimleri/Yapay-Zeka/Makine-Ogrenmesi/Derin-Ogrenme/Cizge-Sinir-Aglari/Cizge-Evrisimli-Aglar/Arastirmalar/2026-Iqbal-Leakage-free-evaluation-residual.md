---
research_id: arxiv:2611.04660
title: "Leakage-free evaluation of residual graph convolutional networks for network intrusion detection"
authors: ["Zahid Iqbal"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-03
doi:
arxiv: 2611.04660
url: https://arxiv.org/abs/2611.04660
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: graph-convolutional-networks
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.04660"]
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

# Leakage-free evaluation of residual graph convolutional networks for network intrusion detection

## 1. Araştırmanın özeti

> Graph neural networks are increasingly proposed for network intrusion detection, yet many reported results come from protocols in which test flows shape the graph used for training, duplicated flows sit on both sides of the split, or a single split is reported. This study measures what a residual graph convolutional network gains over simpler models once these sources of optimism are removed. CICIDS2017 and NF-UNSW-NB15-v2 were cleaned with label-aware removal of exact duplicates, removing 69% of NF-UNSW-NB15-v2 flows. Flows were linked in a nearest-neighbour graph built from training flows only, and validation and test flows were attached to their nearest training flows at prediction time. A two-layer residual network was compared with eight models under the same settings, including a nearest-neighbour vote over the same graph, gradient-boosted trees and a random forest, over three seeds that each draw a new split, with ablations, leave-one-family-out and feature-noise tests. On CICIDS2017 the residual network reached a binary F1 of 98.11% (SD 0.18) and on NF-UNSW-NB15-v2 90.57% (0.38), indistinguishable from a multilayer perceptron without the graph and from other graph networks. Tree ensembles were 1.48 to 1.57 F1 points higher on CICIDS2017 and led on the area under the precision-recall curve on both datasets; their CICIDS2017 multiclass macro-F1 reached 93.08% against 64.51%, a gap mainly from benign flows the residual network assigned to small attack classes. No ablation, including transductive graph construction, changed F1 beyond seed variation. Under Gaussian feature noise (SD 0.5), the residual network kept an F1 of 96.16%, while XGBoost fell to 0.67%. Under a leakage-controlled protocol, message passing over flow graphs adds no measurable accuracy over a perceptron, and tree ensembles remain stronger on both; the advantage of graph models lies in robustness to feature noise.

*Özet kaynağı: arxiv:2611.04660 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çizge Evrişimli Ağlar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.04660
- Metadata kaynakları: arxiv:2611.04660 (toplama: 2026-11-05)
