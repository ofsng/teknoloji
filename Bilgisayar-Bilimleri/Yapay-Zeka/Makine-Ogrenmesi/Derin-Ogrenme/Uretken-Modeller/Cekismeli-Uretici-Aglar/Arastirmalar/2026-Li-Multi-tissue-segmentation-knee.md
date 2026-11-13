---
research_id: doi:10.3389/fmolb.2026.1913664
title: "Multi-tissue segmentation of knee MRI based on U-Net and conditional generative adversarial networks"
authors: ["Songjia Li", "Weiwei Ma", "jiacheng xu", "Yong Xiong", "Yipu Luo", "Minghan Li"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-06
doi: 10.3389/fmolb.2026.1913664
arxiv:
url: https://doi.org/10.3389/fmolb.2026.1913664
publication: "Frontiers in Molecular Biosciences"
publication_type: article
peer_reviewed: true
primary_technology: generative-adversarial-networks
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["knee MRI", "U-Net", "conditional generative adversarial networks", "knee cartilage segmentation", "femur segmentation", "loss functions", "normalization strategies", "boundary accuracy", "cartilage structure"]
source_ids: ["openalex:W7225171014"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-13
last_checked_at: 2026-11-13
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-13
---

# Multi-tissue segmentation of knee MRI based on U-Net and conditional generative adversarial networks

## 1. Araştırmanın özeti

> Objective This study aimed to systematically compare the performance of U-Net and a conditional generative adversarial network (cGAN) for multi-tissue segmentation of knee magnetic resonance imaging (MRI) using the public SKI10 dataset, and to investigate the effects of loss functions, discriminator receptive fields, and normalization strategies on model performance through ablation experiments. Methods The segmentation targets included the femur, femoral cartilage, tibia, and tibial cartilage, with the background incorporated as an additional class to formulate a five-class segmentation task. All MRI images and labels were read from the original. mhd files and two-dimensional slices were extracted along the sagittal direction. Images were resized to 512 × 512 pixels and standardized using z-score normalization, whereas labels were resized with nearest-neighbor interpolation to preserve categorical encoding. Training and test sets were split at the MRI-volume level to prevent information leakage caused by adjacent slices from the same volume being assigned to different subsets. U-Net was used as the supervised baseline model, and a cGAN segmentation framework consisting of a U-Net-style generator and a discriminator was constructed. Evaluation metrics included the Dice similarity coefficient (DSC) and the 95th-percentile Hausdorff distance (HD95). Qualitative segmentation, error heatmaps, boundary comparison, per-class win rate, Bland-Altman agreement analysis, boundary DSC, false-positive/false-negative composition, surface-distance distributions, and training dynamics were further analyzed. A sub-selection of 10 of the 70 training volumes was used as a validation set for checkpoint selection; the 30 test volumes were accessed only at final evaluation and were never used for training, model selection, or hyperparameter optimisation. Results Baseline comparison showed that U-Net and cGAN exhibited complementary behavior in knee MRI multi-tissue segmentation. The mean DSC across the four anatomical structures was significantly higher for cGAN than for U-Net (0.8061 ± 0.0542 vs. 0.8035 ± 0.0520; P < 0.001). In contrast, the mean HD95 was lower for cGAN than for U-Net (4.02 ± 1.18 mm vs. 5.38 ± 1.44 mm), indicating better boundary-distance control and local contour fitting. Structure-specific analysis showed that segmentation of osseous structures was more stable than that of cartilage structures, and model differences were concentrated mainly in thin-layer tissues such as femoral and tibial cartilage. Loss-function ablation showed that L2 and Smooth L1 losses improved DSC and reduced HD95 in U-Net, with Smooth L1 being more favorable for boundary-distance control. In the cGAN framework, the L1 pixel-wise loss yielded the most stable performance. Discriminator receptive-field ablation showed that PixelGAN achieved the best overall performance, indicating that larger PatchGAN receptive fields do not necessarily improve segmentation of medical label maps. Comparison of normalization strategies showed that BatchNorm achieved higher DSC than InstanceNorm in both U-Net and cGAN PixelGAN. Conclusion U-Net and cGAN showed complementary strengths in knee MRI multi-tissue segmentation. U-Net provided better regional overlap and cartilage continuity, whereas cGAN PixelGAN achieved lower boundary errors. These findings support task-specific selection of segmentation architectures and discriminator configurations. However, as the results were based on a single predefined volume-level split of the SKI10 dataset, they require confirmation through repeated splits, cross-validation, and external multicenter validation.

*Özet kaynağı: openalex:W7225171014 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çekişmeli Üretici Ağlar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3389/fmolb.2026.1913664
- OpenAlex: https://openalex.org/W7225171014
- Metadata kaynakları: openalex:W7225171014 (toplama: 2026-11-13)
