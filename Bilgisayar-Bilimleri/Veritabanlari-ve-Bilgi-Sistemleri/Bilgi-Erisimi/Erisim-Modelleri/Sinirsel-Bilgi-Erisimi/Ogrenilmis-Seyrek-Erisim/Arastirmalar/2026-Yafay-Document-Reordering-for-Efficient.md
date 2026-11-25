---
research_id: doi:10.1109/access.2026.3690983
title: "Document Reordering for Efficient Dynamic Pruning in Traditional and Learned Sparse Retrieval"
authors: ["Erman Yafay", "İsmail Sengör Altıngövde"]
year: 2026
published_date: 2026-01-01
updated_date: 2026-11-10
doi: 10.1109/access.2026.3690983
arxiv:
url: https://doi.org/10.1109/access.2026.3690983
publication: "IEEE Access"
publication_type: article
peer_reviewed: true
primary_technology: learned-sparse-retrieval
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["dynamic pruning", "top-k retrieval", "document frequency", "BM25", "SPLADE", "learned sparse retrieval", "neural retrieval", "inverted index", "query efficiency"]
source_ids: ["openalex:W7160432055"]
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

# Document Reordering for Efficient Dynamic Pruning in Traditional and Learned Sparse Retrieval

## 1. Araştırmanın özeti

> Large scale Web search engines conduct first-stage retrieval using a traditional inverted index, on which they are expected to execute billions of queries on a very tight budget, i.e., less than 200 milliseconds. During query processing, the postings lists corresponding to each query term are traversed in parallel, i.e., applying document-at-a-time (DaaT) strategy, and a min-heap of top-kdocuments is employed to store the top-ranked documents. Dynamic pruning algorithms accelerate DaaT query processing by skipping documents that cannot enter the top-kresults. Their efficiency, however, depends on how quickly the heap threshold increases during scoring. This paper explores an alternative route to faster pruning: rather than estimating the threshold in advance, we reorder documents within postings lists so that most frequently retrieved documents are encountered earlier, allowing the threshold to rise more rapidly. We show that the proposedHit Count(HC) reordering—derived from document frequency in historical query logs—achieves comparable speedups for both traditional and learned sparse models. Specifically, HC provides up to a 1.12× speed-up for BM25-based scoring on ClueWeb09B and SPLADE-based scoring on MS MARCO, with only a modest increase in index size. This demonstrates that our lightweight document reordering approach yields consistent efficiency gains in both traditional and neural information retrieval settings.

*Özet kaynağı: openalex:W7160432055 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Öğrenilmiş Seyrek Erişim](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1109/access.2026.3690983
- OpenAlex: https://openalex.org/W7160432055
- Metadata kaynakları: openalex:W7160432055 (toplama: 2026-11-23)
