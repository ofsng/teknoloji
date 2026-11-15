---
research_id: doi:10.3390/app162110900
title: "GapDPO: Setwise Direct Preference Optimization for LLM Safety Alignment"
authors: ["Hyeongsoo Lim", "Jinyoung Kim", "Min Ho Jang", "Minji Cho", "Eun Seo Seo", "Ji Won Yoon"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-05
doi: 10.3390/app162110900
arxiv:
url: https://doi.org/10.3390/app162110900
publication: "Applied Sciences"
publication_type: article
peer_reviewed: true
primary_technology: direct-preference-optimization
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["direct preference optimization", "HarmBench"]
source_ids: ["openalex:W7225156821"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-09
last_checked_at: 2026-11-09
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-09
---

# GapDPO: Setwise Direct Preference Optimization for LLM Safety Alignment

## 1. Araştırmanın özeti

> While reinforcement learning is widely used to align large language models (LLMs), its application to open-ended settings remains limited by reliance on preference datasets, making it difficult to scale to non-reasoning tasks such as safety. Applying direct preference optimization (DPO) to LLM safety alignment requires preferred and dispreferred responses for harmful instructions, making scalable preference construction a key bottleneck. We therefore propose GapDPO, a setwise preference optimization method that enables DPO-based safety alignment without reward models, verifiers, or preference annotation. GapDPO constructs preference sets by generating safe responses with our proposed refusal-style prompts and pairing them with affirmative targets from the dataset. GapDPO then maximizes the mean reward gap between the two sets while penalizing within-set variance. On AdvBench and HarmBench, GapDPO reduces the average attack success rate under PAIR, GCG, and AmpleGCG from 21.3% for refusal-style fine-tuning and 15.0% for single-pair DPO to 10.6%, while increasing strict set separation on training behaviors from 51% to as high as 63%. The improvement is mainly observed under GCG attacks and is accompanied by more refusals of benign requests. The averaged pairwise DPO on the same preference sets performs comparably, indicating that these sets account for most of the gain over single-pair DPO.

*Özet kaynağı: openalex:W7225156821 — lisans: cc-by. Tam metin incelenmedi.*

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
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/app162110900
- OpenAlex: https://openalex.org/W7225156821
- Metadata kaynakları: openalex:W7225156821 (toplama: 2026-11-09)
