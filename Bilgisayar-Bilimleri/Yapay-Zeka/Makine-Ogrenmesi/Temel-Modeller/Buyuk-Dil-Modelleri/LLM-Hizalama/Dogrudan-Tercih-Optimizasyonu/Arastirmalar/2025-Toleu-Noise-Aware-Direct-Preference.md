---
research_id: doi:10.3390/app151910328
title: "Noise-Aware Direct Preference Optimization for RLAIF"
authors: ["Alymzhan Toleu", "Gulmira Tolegen", "Alexandr Pak", "Assel Jaxylykova"]
year: 2025
published_date: 2025-09-23
updated_date: 2026-10-14
doi: 10.3390/app151910328
arxiv:
url: https://doi.org/10.3390/app151910328
publication: "Applied Sciences"
publication_type: article
peer_reviewed: true
primary_technology: direct-preference-optimization
related_technologies: ["reinforcement-learning"]
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["reinforcement learning from AI feedback", "direct preference optimization", "label noise", "AI alignment"]
source_ids: ["openalex:W4414425991"]
cited_by_count: 1
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-15
last_checked_at: 2026-11-15
content_verified: false
identifier_verified: false
---

# Noise-Aware Direct Preference Optimization for RLAIF

## 1. Araştırmanın özeti

> Reinforcement Learning from Human Feedback (RLHF) produces powerful instruction-following models but relies on a preference-labeling process that is both costly and slow. An effective alternative, Reinforcement Learning from AI Feedback (RLAIF), uses large language models as teachers for relabeling; however, this introduces substantial label noise. In our setting, we found that AI teachers flipped approximately 50% of the original human preferences on the dataset, a condition that degrades the performance of standard direct preference optimization (DPO). We propose noise-robust DPO (nrDPO) and nrDPO-gated, two drop-in variants that make DPO resilient to noisy preferences. nrDPO reweights each pair by (i) a margin-confidence term from a frozen reference policy (base or SFT), (ii) a context-stability term that penalizes preferences that change under truncated histories, and (iii) a length correction to curb verbosity bias. nrDPO-gated further filters low-confidence pairs via a simple threshold on the reference margin. On a dataset with heavy synthetic noise (30% flips), nrDPO-gated improves the preference accuracy by +3.8% over vanilla DPO; in a realistic RLAIF setting, nrDPO-gated is the only configuration that recovers competitive alignment, reaching ≈60% on a 5k relabeled set (vs. ≈49–50% for vanilla DPO) and approaching RLHF baselines.

*Özet kaynağı: openalex:W4414425991 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Doğrudan Tercih Optimizasyonu](../_index.md)
- **İlişkili:** [Pekiştirmeli Öğrenme](../../../../../Pekistirmeli-Ogrenme/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/app151910328
- OpenAlex: https://openalex.org/W4414425991
- Metadata kaynakları: openalex:W4414425991 (toplama: 2026-11-15)
