---
research_id: doi:10.1145/3842528
title: "Marigold V2: Revisiting Diffusion Transformers for Monocular Depth Estimation"
authors: ["Igor Pavlovic", "Thiemo Wandel", "Anton Obukhov", "Luca Bartolomei", "Andrey Davydov", "Fabio Tosi", "Matteo Poggi", "Sabine Süsstrunk", "Dengxin Dai"]
year: 2026
published_date: 2026-11-09
updated_date: 2026-11-11
doi: 10.1145/3842528
arxiv: 2609.08084
url: https://doi.org/10.1145/3842528
publication: "ACM Transactions on Graphics"
publication_type: article
peer_reviewed: true
primary_technology: depth-estimation
related_technologies: ["flow-matching"]
classification_confidence: high
classification_method: deterministic
keywords: ["monocular depth estimation", "diffusion transformer", "marigold", "flow matching", "out-of-distribution generalization", "two-stage fine-tuning", "surface normal estimation", "intrinsic image decomposition"]
source_ids: ["openalex:W7212031568"]
cited_by_count: 4
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-12
last_checked_at: 2026-11-12
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-12
---

# Marigold V2: Revisiting Diffusion Transformers for Monocular Depth Estimation

## 1. Araştırmanın özeti

> Monocular depth estimation is a ubiquitous yet highly ill-posed computer vision task, with downstream applications in scene reconstruction, computational photography, and robotics, among others. Despite the field's maturity, recent models still struggle to generalize to out-of-distribution inputs and to produce sharp and detailed depth maps. In this paper, we revisit Marigold, a set of techniques for repurposing modern image generation and editing models, powered by the diffusion transformer (DiT) architecture, into state-of-the-art monocular depth estimators. Our recipes target single-step inference from pretrained multi-step flow-matching models, with quantization where needed, preserving model capacity while remaining cheap to run. We analyze the artifacts of naïve training and identify two effective remedies: aligning the model's internal representations with semantic features extracted from ground-truth, and adopting a 2-stage fine-tuning protocol built around a novel Sinkhorn-based loss. The results are crisper, cleaner depth maps that generalize well out-of-distribution, with 16–26% improvement in AbsRel over the previous best on KITTI and ETH3D. Qualitatively, our model resolves fur, foliage, and hair-thin edges that have eluded prior models. Furthermore, Marigold V2 achieves state-of-the-art results when applied to other dense regression tasks, such as surface normals estimation and intrinsic image decomposition. Project website: https://hf.co/spaces/huawei-bayerlab/marigold-v2-web.

*Özet kaynağı: openalex:W7212031568 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Derinlik Kestirimi](../_index.md)
- **İlişkili:** [Akış Eşleme](../../../../Makine-Ogrenmesi/Derin-Ogrenme/Uretken-Modeller/Difuzyon-Modelleri/Akis-Esleme/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1145/3842528
- arXiv: https://arxiv.org/abs/2609.08084
- OpenAlex: https://openalex.org/W7212031568
- Metadata kaynakları: openalex:W7212031568 (toplama: 2026-11-12)
