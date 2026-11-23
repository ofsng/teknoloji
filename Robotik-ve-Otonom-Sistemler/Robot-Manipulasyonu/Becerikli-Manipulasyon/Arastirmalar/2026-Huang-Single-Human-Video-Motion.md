---
research_id: doi:10.3390/electronics15225403
title: "A Single Human Video as a Motion Prior: Residual Reinforcement Learning and Diffusion Distillation for Vision-Based Dexterous Manipulation"
authors: ["Yantai Huang", "黄生传", "Qingchun Jiao", "Zhenyu Zhang"]
year: 2026
published_date: 2026-11-19
updated_date: 2026-11-22
doi: 10.3390/electronics15225403
arxiv:
url: https://doi.org/10.3390/electronics15225403
publication: Electronics
publication_type: article
peer_reviewed: true
primary_technology: dexterous-manipulation
related_technologies: ["reinforcement-learning"]
classification_confidence: high
classification_method: deterministic
keywords: ["dexterous manipulation", "visual servoing", "motion priors", "residual reinforcement learning", "diffusion distillation", "domain randomization", "policy distillation"]
source_ids: ["openalex:W7236666572"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-23
last_checked_at: 2026-11-23
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-23
---

# A Single Human Video as a Motion Prior: Residual Reinforcement Learning and Diffusion Distillation for Vision-Based Dexterous Manipulation

## 1. Araştırmanın özeti

> Learning dexterous manipulation typically requires hundreds of demonstrations, making data collection costly and hard to scale. We propose a three-stage framework learning from a single human video. First, hand and object trajectories extracted from the video are retargeted to the robot as motion priors. Second, combining residual learning with trajectory augmentation, a privileged state policy is trained via proximal policy optimization to generalize to unseen object poses. Third, a diffusion model distills this policy into a visual controller: the privileged policy collects self-generated successful trajectories under standard and perceptual domain randomization conditions, which are blended to train the diffusion model to output action sequences from raw point clouds. Across three dexterous manipulation tasks, the privileged state policy attains high success rates with one demonstration video per object, achieving higher SR10 success rates than DexMV baselines on the same Adroit platform with two orders of magnitude fewer demonstrations, while the distilled vision-based policy operates from raw point clouds without privileged state information. This work demonstrates that effective dexterous manipulation strategies can be learned even when human supervision is limited to a single demonstration video. The video supplies the motion prior, while all the remaining training experience, including the robot rollouts that are used for distillation, is generated autonomously in simulation. This offers a practical pathway for low-cost robotic skill learning.

*Özet kaynağı: openalex:W7236666572 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Becerikli Manipülasyon](../_index.md)
- **İlişkili:** [Pekiştirmeli Öğrenme](../../../../Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Pekistirmeli-Ogrenme/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/electronics15225403
- OpenAlex: https://openalex.org/W7236666572
- Metadata kaynakları: openalex:W7236666572 (toplama: 2026-11-23)
