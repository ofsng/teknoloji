---
research_id: doi:10.3390/info17111135
title: "Multi-Armed Bandit-Based Model Selection for Incremental Phishing Detection: An Empirical Study of Accuracy, Cost, and Concept Drift"
authors: ["Mutaz A. B. Al-Tarawneh", "Ajla Kulaglic", "Rand Ibrahim Al-Suhimat"]
year: 2026
published_date: 2026-11-11
updated_date: 2026-11-13
doi: 10.3390/info17111135
arxiv:
url: https://doi.org/10.3390/info17111135
publication: Information
publication_type: article
peer_reviewed: true
primary_technology: multi-armed-bandits
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["phishing detection", "multi-armed bandits", "online model selection", "incremental learning", "concept drift", "cost-sensitive learning", "Mondrian Forest", "adaptive random forest", "majority voting", "URL classification"]
source_ids: ["openalex:W7167728256"]
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

# Multi-Armed Bandit-Based Model Selection for Incremental Phishing Detection: An Empirical Study of Accuracy, Cost, and Concept Drift

## 1. Araştırmanın özeti

> Phishing websites are generated quickly and change their appearance to evade detection, so detectors must keep learning after deployment. Incremental learning allows a detector to update with every labeled instance, but which incremental learner to deploy is rarely known in advance, and running a full ensemble of learners increases latency and memory. This paper proposes and empirically evaluates a multi-armed bandit (MAB)-based online model selection framework for resource-aware incremental phishing detection, in which heterogeneous incremental learners are treated as arms and a bandit policy chooses the learner that classifies each incoming instance. The framework combines ten bandit policies, including three drift-aware policies, with three model-update strategies (selected-only, hybrid, all-model) and three reward designs: accuracy-based, cost-sensitive, and resource-aware, where the last penalizes the processing time and memory of the selected learner. The framework is evaluated prequentially on two phishing datasets (10,000 and 21,891 instances) under stationary streams, five controlled drift scenarios injected into the real datasets, and two synthetic drift benchmarks, using repeated runs and non-parametric statistical tests, against six individual learners, Adaptive Random Forest, Streaming Random Patches, majority-vote and Hedge ensembles, and a warm-up selection baseline. An Aggregated Mondrian Forest achieved the highest Cohen’s kappa among the individual learners on all shuffled and drifting phishing streams (kappa 0.907 and 0.457 on the stationary streams), and only a Hedge ensemble of all six learners matched it, at 2.5–4.7 times its processing time. Under all-model update the bandit came within about 0.02 kappa of the best learner without knowing it in advance. The oracle analysis showed that the best learner changed rarely on most streams; where it did change, namely when the most informative URL features of the second dataset became unavailable, a drift-aware policy made fewer errors than any fixed learner. Because the drift was injected, these results show how the policies respond to known types of change, not how they would perform on a continuously evolving phishing feed. The update strategy determined the processing cost (0.9–12.6 ms per instance), and the resource-aware reward shifted selection predictably toward cheaper learners, yielding tunable operating points. The results position MAB-based selection as a controllable cost–accuracy mechanism for incremental phishing detection whose benefit grows with the variability of the best learner and of the resource budget.

*Özet kaynağı: openalex:W7167728256 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çok Kollu Haydutlar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/info17111135
- OpenAlex: https://openalex.org/W7167728256
- Metadata kaynakları: openalex:W7167728256 (toplama: 2026-11-14)
