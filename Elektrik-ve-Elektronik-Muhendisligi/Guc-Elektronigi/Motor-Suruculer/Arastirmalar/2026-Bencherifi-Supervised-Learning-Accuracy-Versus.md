---
research_id: doi:10.3390/act15110592
title: "Supervised Learning Accuracy Versus Closed-Loop Control Performance in Neural Behavioral Cloning of an Integral Sliding-Mode Controller for an Induction Motor Drive"
authors: ["Said Bencherifi", "Azzeddine Dekhane", "Mohamed Faouzi Rachedi", "Habib Benbouhenni", "Riyadh Bouddou", "Jun Jiat Tiang"]
year: 2026
published_date: 2026-11-06
updated_date: 2026-11-21
doi: 10.3390/act15110592
arxiv:
url: https://doi.org/10.3390/act15110592
publication: Actuators
publication_type: article
peer_reviewed: true
primary_technology: motor-drives
related_technologies: ["sliding-mode-control"]
classification_confidence: high
classification_method: deterministic
keywords: ["integral sliding mode control", "induction motor drive", "closed-loop performance", "speed control", "anti-windup", "actuator saturation", "parameter perturbation", "data-driven control"]
source_ids: ["openalex:W7225660837"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-22
last_checked_at: 2026-11-22
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-22
---

# Supervised Learning Accuracy Versus Closed-Loop Control Performance in Neural Behavioral Cloning of an Integral Sliding-Mode Controller for an Induction Motor Drive

## 1. Araştırmanın özeti

> Artificial intelligence (AI)-based control is gaining increasing attention in electrical-machine drives as a means of approximating nonlinear control laws through data-driven learning. Neural behavioral cloning provides a practical framework for reproducing an existing analytical controller while retaining the established control architecture. However, neural controllers are typically selected according to supervised validation loss, despite the fact that its ability to predict closed-loop control performance remains unclear. This paper systematically investigates the relationship between supervised learning accuracy and closed-loop performance through neural behavioral cloning of an integral sliding-mode speed controller for a 2.2 kW field-oriented induction motor drive. A bias-free, odd-symmetric neural network is trained to approximate the analytical control law, while the integral state, state-update law, anti-windup mechanism, actuator saturation, execution sequence, and controller lifecycle are kept identical in the analytical and neural implementations, thereby isolating the effect of the learned approximation on closed-loop behavior. The controllers are evaluated under ten benchmark conditions comprising nominal operation, six individual parameter perturbations, and a combined worst-case condition, with the sliding-surface coefficient selected equal to the PI design bandwidth parameter. Across five trained networks, whose validation mean-squared errors span a factor of 2.4, supervised validation accuracy exhibits only a weak relationship with closed-loop performance. The largest ITAE variation among the five networks within any benchmark cell is 1.60% of the corresponding cell median, while the network with the highest validation error yields the lowest ITAE in nine of the ten benchmark cells. Nevertheless, all neural controllers closely reproduce the analytical controller and achieve a 39–68% reduction in ITAE relative to a conventional proportional–integral controller, with a median reduction of 49% across the ten benchmark cells. These results indicate that, within the investigated setting, supervised validation loss is not a reliable criterion for ranking behaviorally cloned controllers according to their closed-loop performance. The findings are limited to a single induction motor drive, one teacher controller, one network architecture (H = 16), and five trained networks representing two distinct validation-error groups; broader conclusions require systematic evaluation across architectures, teacher controllers, drive conditions, and training configurations.

*Özet kaynağı: openalex:W7225660837 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Motor Sürücüler](../_index.md)
- **İlişkili:** [Kayan Kipli Kontrol](../../../../Mekatronik-ve-Kontrol-Sistemleri/Kontrol-Teorisi/Dogrusal-Olmayan-Kontrol/Kayan-Kipli-Kontrol/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/act15110592
- OpenAlex: https://openalex.org/W7225660837
- Metadata kaynakları: openalex:W7225660837 (toplama: 2026-11-22)
