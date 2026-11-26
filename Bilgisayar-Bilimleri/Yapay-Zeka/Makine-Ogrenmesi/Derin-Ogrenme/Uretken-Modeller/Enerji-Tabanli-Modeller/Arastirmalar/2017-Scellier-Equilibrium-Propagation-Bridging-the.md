---
research_id: doi:10.3389/fncom.2017.00024
title: "Equilibrium Propagation: Bridging the Gap between Energy-Based Models and Backpropagation"
authors: ["Benjamin Scellier", "Yoshua Bengio"]
year: 2017
published_date: 2017-05-04
updated_date: 2026-11-23
doi: 10.3389/fncom.2017.00024
arxiv: 1602.05179
url: https://doi.org/10.3389/fncom.2017.00024
publication: "Frontiers in Computational Neuroscience"
publication_type: article
peer_reviewed: true
primary_technology: energy-based-models
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["equilibrium propagation", "energy-based models", "backpropagation", "contrastive divergence", "gradient computation", "error back-propagation", "spike-timing-dependent plasticity", "recurrent neural networks", "supervised learning", "MNIST", "fixed point computation", "synaptic plasticity"]
source_ids: ["openalex:W2527798464"]
cited_by_count: 886
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-23
last_checked_at: 2026-11-23
content_verified: false
identifier_verified: crossref
---

# Equilibrium Propagation: Bridging the Gap between Energy-Based Models and Backpropagation

## 1. Araştırmanın özeti

> We introduce Equilibrium Propagation, a learning framework for energy-based models. It involves only one kind of neural computation, performed in both the first phase (when the prediction is made) and the second phase of training (after the target or prediction error is revealed). Although this algorithm computes the gradient of an objective function just like Backpropagation, it does not need a special computation or circuit for the second phase, where errors are implicitly propagated. Equilibrium Propagation shares similarities with Contrastive Hebbian Learning and Contrastive Divergence while solving the theoretical issues of both algorithms: our algorithm computes the gradient of a well-defined objective function. Because the objective function is defined in terms of local perturbations, the second phase of Equilibrium Propagation corresponds to only nudging the prediction (fixed point or stationary distribution) toward a configuration that reduces prediction error. In the case of a recurrent multi-layer supervised network, the output units are slightly nudged toward their target in the second phase, and the perturbation introduced at the output layer propagates backward in the hidden layers. We show that the signal "back-propagated" during this second phase corresponds to the propagation of error derivatives and encodes the gradient of the objective function, when the synaptic update corresponds to a standard form of spike-timing dependent plasticity. This work makes it more plausible that a mechanism similar to Backpropagation could be implemented by brains, since leaky integrator neural computation performs both inference and error back-propagation in our model. The only local difference between the two phases is whether synaptic changes are allowed or not. We also show experimentally that multi-layer recurrently connected networks with 1, 2, and 3 hidden layers can be trained by Equilibrium Propagation on the permutation-invariant MNIST task.

*Özet kaynağı: openalex:W2527798464 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Enerji Tabanlı Modeller](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3389/fncom.2017.00024
- arXiv: https://arxiv.org/abs/1602.05179
- OpenAlex: https://openalex.org/W2527798464
- Metadata kaynakları: openalex:W2527798464 (toplama: 2026-11-23)
