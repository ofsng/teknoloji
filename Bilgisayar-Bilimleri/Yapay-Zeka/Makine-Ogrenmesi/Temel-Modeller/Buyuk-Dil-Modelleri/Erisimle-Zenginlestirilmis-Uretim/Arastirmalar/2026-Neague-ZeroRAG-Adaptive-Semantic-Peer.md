---
research_id: doi:10.1145/3801927.3858412
title: "ZeroRAG: Adaptive Semantic Peer Routing for Decentralized Retrieval-Augmented Generation"
authors: ["Petru Neague", "Quinten Stokkink", "Martijn de Vos", "Rafael Pires", "Mathis Randl", "Anne-Marie Kermarrec", "Johan Pouwelse"]
year: 2026
published_date: 2026-11-05
updated_date: 2026-11-05
doi: 10.1145/3801927.3858412
arxiv: 2611.07928
url: https://arxiv.org/abs/2611.07928
publication: arXiv
publication_type: preprint
peer_reviewed:
primary_technology: retrieval-augmented-generation
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.07928"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: [{"relation": "published_version", "doi": "10.1145/3801927.3858412", "source": "arxiv"}]
collected_at: 2026-11-07
last_checked_at: 2026-11-07
content_verified: false
identifier_verified: not_found
retraction_checked: 2026-11-07
---

# ZeroRAG: Adaptive Semantic Peer Routing for Decentralized Retrieval-Augmented Generation

## 1. Araştırmanın özeti

> Retrieval-augmented generation (RAG) is a standard approach to enhance the reliability of large language model (LLM) outputs by retrieving documents relevant to a query and supplying them in the LLM prompt. Today's RAG systems collect, index, and serve these documents from centralized stores. In practice, however, documents are owned by organizations, devices, and individuals who cannot or will not surrender custody of them to a central party, e.g., because of privacy, copyright or regulatory compliance. Existing modern decentralized retrieval techniques either reintroduce a coordinating authority, or rely on a global data structure that requires continuous network-wide coordination (e.g., DHTs). We present ZeroRAG, a decentralized routing layer for document retrieval in RAG that performs semantic query routing across an overlay of peers with- out global data structures or centralized orchestration. Documents remain with the peers that own them, and each peer keeps only lightweight local state: a bounded set of neighbor advertisements and a cache of recently routed queries. Using these, ZeroRAG steers each query through a best-first walk that progressively rewires the overlay toward semantically relevant neighbors, so recall improves over time as the network self-organizes. We evaluate ZeroRAG using three real-world workloads and two decentralized baselines. We find that ZeroRAG outperforms baselines in terms of recall and required network messages, approaches the recall and LLM answer accuracy of a centralized document store, self-heals after catastrophic peer failures, and scales to 100 000 peers.

*Özet kaynağı: arxiv:2611.07928 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Erişimle Zenginleştirilmiş Üretim](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1145/3801927.3858412
- arXiv: https://arxiv.org/abs/2611.07928
- Yayımlanmış sürüm: https://doi.org/10.1145/3801927.3858412
- Metadata kaynakları: arxiv:2611.07928 (toplama: 2026-11-07)
