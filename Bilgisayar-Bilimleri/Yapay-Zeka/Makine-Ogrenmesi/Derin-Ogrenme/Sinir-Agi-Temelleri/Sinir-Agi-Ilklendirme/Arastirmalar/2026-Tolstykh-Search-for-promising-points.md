---
research_id: doi:10.17586/2226-1494-2026-26-5-993-999
title: "Search for promising points of neural networks initialization"
authors: ["Victor N. Tolstykh", "Vladimir N. Yershov"]
year: 2026
published_date: 2026-10-25
updated_date: 2026-11-21
doi: 10.17586/2226-1494-2026-26-5-993-999
arxiv:
url: https://doi.org/10.17586/2226-1494-2026-26-5-993-999
publication: "Scientific and technical journal of information technologies mechanics and optics"
publication_type: article
peer_reviewed: true
primary_technology: neural-network-initialization
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["neural network initialization", "gradient descent", "local minima", "saddle points", "error function", "perceptron", "single hidden layer", "learning speed", "Hessian-free optimization", "restricted Boltzmann machine"]
source_ids: ["openalex:W7223690136"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-23
last_checked_at: 2026-11-23
content_verified: false
identifier_verified: crossref
---

# Search for promising points of neural networks initialization

## 1. Araştırmanın özeti

> The paper examines the problem of initialization, which consists in determining the starting point in the space of the neural network weights for a qualitative gradient descent. It is known that the learning speed and learning result of a neural network mostly depends on its initialization. The problem is that in the process of execution, the algorithm can get into the anomalous zone of the local minimum and get stuck there for a long time, sometimes at the very beginning of training. In such cases, it is recommended to start the descent with a new initialization. The study proposes to start training from a point at the bottom of the local minimum, from which, as research shows, the descent in a new direction begins. The proposed method is based on the assumption that most of these anomalies are critical points that have a direction to descent. The neural network is initialized every time the learning algorithm encounters an anomaly in which the value of the error function increases. At the same time, a new initialization is determined at the minimum point of the error function in the segment connecting the point before the anomaly and the following one. Successive initializations result in the descent occurring along an optimized trajectory without significant oscillations. The effectiveness of the method is demonstrated by the example of a perceptron with a single hidden layer and one anomaly. It is proved that the descent from the new initialization point is faster; this demonstrates the possibility of gradient correction without calculating the Hessian; a conclusion is made about the expediency of multiple initializations of the neural network when it enters the zone of the next anomaly. It is proposed to use the method of correcting the gradient descent algorithm to reach the bottom of the anomaly in cases where the error begins to grow. The developed method gives a high probability of hitting a region with a low value of the error function than in the case of a random drawing of the initialization point, as well as a benefit in comparison with a Restricted Boltzmann’s machine in terms of execution time.

*Özet kaynağı: openalex:W7223690136 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Sinir Ağı İlklendirme](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.17586/2226-1494-2026-26-5-993-999
- OpenAlex: https://openalex.org/W7223690136
- Metadata kaynakları: openalex:W7223690136 (toplama: 2026-11-23)
