---
research_id: arxiv:2611.29399
title: "SJG: A Skyline Joint Graph for Multi-Component Approximate Nearest Neighbor Search"
authors: ["Linyun Ma", "Rui Mao"]
year: 2026
published_date: 2026-11-22
updated_date: 2026-11-22
doi:
arxiv: 2611.29399
url: https://arxiv.org/abs/2611.29399
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: approximate-nearest-neighbor-search
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.29399"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-24
last_checked_at: 2026-11-24
content_verified: false
identifier_verified: arxiv
---

# SJG: A Skyline Joint Graph for Multi-Component Approximate Nearest Neighbor Search

## 1. Araştırmanın özeti

> Graph-based indexes enable efficient approximate nearest neighbor search at scale by linking similar objects. In applications such as product retrieval and rental listing search, similarity depends on several components whose relative importance varies across queries. The challenge is that the index must select neighbors during construction, but the query weights that determine which objects are closest are not yet known. A straightforward approach is to index each component separately. However, merging the results of these searches can miss the nearest neighbor under the weighted distance. A joint graph allows a search to follow links across components, helping to avoid such misses, but selecting neighbors separately within each component can leave redundant edges, and keeping component hierarchies synchronized limits parallel construction. To address these limitations, we propose the Skyline Joint Graph (SJG). Although query weights can change the ranking of candidate neighbors, the dominance relation among them is independent of those weights. SJG exploits this property by pooling candidates across components and retaining the Skyline for each node, thereby enabling efficient approximate nearest neighbor search under different query weights while supporting parallel graph construction. Extensive experiments on six real-world datasets demonstrate that SJG achieves up to $27.9\times$ the query throughput of baseline methods at 90% Recall@10, while accelerating single-threaded index construction by up to $201\times$. Its index requires at least 36% less space than the smallest baseline index.

*Özet kaynağı: arxiv:2611.29399 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Yaklaşık En Yakın Komşu Arama](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.29399
- Metadata kaynakları: arxiv:2611.29399 (toplama: 2026-11-24)
