---
research_id: arxiv:2611.08383
title: "FedReason: Large Language Models as Weight-Space Meta-Aggregators for Heterogeneous Federated Learning"
authors: ["Ali Mohammadi Ruzbahani", "Abbas Yazdinejad", "Hadis Karimipour"]
year: 2026
published_date: 2026-11-05
updated_date: 2026-11-05
doi:
arxiv: 2611.08383
url: https://arxiv.org/abs/2611.08383
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: large-language-models
related_technologies: ["federated-learning"]
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.08383"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-07
last_checked_at: 2026-11-07
content_verified: false
identifier_verified: arxiv
---

# FedReason: Large Language Models as Weight-Space Meta-Aggregators for Heterogeneous Federated Learning

## 1. Araştırmanın özeti

> Federated learning servers combine client models with a fixed aggregation rule, and each rule in common use is designed for one kind of heterogeneity. We study whether a large language model (LLM) that inspects the client models can choose the rule itself, without any training on the server. In FedReason, the LLM is called every ten rounds. It analyses the weights by running code in a restricted server-side sandbox, sees only the printed results, may score a few candidates on a 500-image proxy set, and submits a short Python aggregation program. The server applies the program until the next call and falls back to FedAvg whenever its output is invalid. Full weight tensors never leave the server. We evaluated FedReason with Claude Opus 5.5 on CIFAR-10 and CIFAR-100 with ResNet-18 under Dirichlet label skew, width-heterogeneous sub-models and Byzantine clients, in 168 runs against 14 baselines. Across 12 paired label-skew runs it beat FedAvg by 1.26 percentage points on average (10 wins), and a control that spends the same per-round proxy budget on choosing among standard rules by 1.08 points. It was the strongest server-side rule on CIFAR-100 but did not beat SCAFFOLD, which changes client training. With three of ten clients malicious, it excluded all sign-flipping clients from the first round and stayed about one point below FLTrust without training a root model. Without proxy feedback, accuracy fell from 73.8% to 38.8% in one seed. A 60-round run cost 0.79 USD in API fees on average.

*Özet kaynağı: arxiv:2611.08383 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Büyük Dil Modelleri](../_index.md)
- **İlişkili:** [Federe Öğrenme](../../../Federe-Ogrenme/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.08383
- Metadata kaynakları: arxiv:2611.08383 (toplama: 2026-11-07)
