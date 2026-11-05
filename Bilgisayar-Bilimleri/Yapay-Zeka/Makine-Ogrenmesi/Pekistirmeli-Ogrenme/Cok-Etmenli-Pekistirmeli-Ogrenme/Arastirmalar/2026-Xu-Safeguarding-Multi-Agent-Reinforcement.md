---
research_id: arxiv:2611.04957
title: "Safeguarding Multi-Agent Reinforcement Learning for Connected and Automated Vehicles with Recursively Feasible Control Barrier Functions"
authors: ["Jianye Xu", "Yousef Sayed", "Bassam Alrifaee"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-03
doi:
arxiv: 2611.04957
url: https://arxiv.org/abs/2611.04957
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: multi-agent-reinforcement-learning
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.04957"]
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

# Safeguarding Multi-Agent Reinforcement Learning for Connected and Automated Vehicles with Recursively Feasible Control Barrier Functions

## 1. Araştırmanın özeti

> Multi-Agent Reinforcement Learning (MARL) shows promise in coordinating connected and automated vehicles but offers no safety guarantee. Although Control Barrier Functions (CBFs) can add this guarantee, their optimization problem can become infeasible in practice due to control bounds. Moreover, they often overapproximate vehicle and road geometry, which makes them conservative. This paper proposes the Backup-Horizon CBF (BH-CBF), which evaluates safety along a horizon until all vehicles stop. BH-CBF is recursively feasible under control bounds, and it considers the exact vehicle and road geometry. Based on BH-CBF, we derive a fully decentralized safety filter that only needs a single broadcast of vehicle states and routes per step and stays real-time in dense traffic. We use BH-CBF to safeguard a MARL policy over its life cycle: as a reward during pre-training, as a run-time filter at deployment, and as a filter in the training loop that keeps fine-tuning on unseen maps collision-free. In simulations on real-world maps of a roundabout and an intersection, BH-CBF avoids all collisions of unsafe MARL policies and keeps its safety guarantee at every step. Existing filters either collide, lose the guarantee, or fall back to full braking far more often. In recorded roundabout traffic with 1264 human-driven vehicles over 115 km, our safeguarded policies shorten the median travel time by 14% compared with the human drivers, without any collision.

*Özet kaynağı: arxiv:2611.04957 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çok Etmenli Pekiştirmeli Öğrenme](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.04957
- Metadata kaynakları: arxiv:2611.04957 (toplama: 2026-11-05)
