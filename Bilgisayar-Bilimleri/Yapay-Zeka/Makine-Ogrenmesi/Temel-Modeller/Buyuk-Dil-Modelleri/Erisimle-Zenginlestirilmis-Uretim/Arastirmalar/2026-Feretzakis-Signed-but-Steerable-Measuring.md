---
research_id: arxiv:2611.06498
title: "Signed but Steerable: Measuring and Closing the Text-Vector Integrity Gap in Offline Retrieval-Augmented Generation"
authors: ["Georgios Feretzakis", "Alexandros Papaspyridis"]
year: 2026
published_date: 2026-11-04
updated_date: 2026-11-04
doi:
arxiv: 2611.06498
url: https://arxiv.org/abs/2611.06498
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: retrieval-augmented-generation
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.06498"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-06
last_checked_at: 2026-11-06
content_verified: false
identifier_verified: arxiv
---

# Signed but Steerable: Measuring and Closing the Text-Vector Integrity Gap in Offline Retrieval-Augmented Generation

## 1. Araştırmanın özeti

> Offline retrieval-augmented generation (RAG) on edge devices is updated through signed knowledge packs that carry text and precomputed embedding vectors. A signature proves who published a pack, not that its vectors encode its text. We study this text-vector integrity gap. A verifier that recomputes vectors and accepts them within a cosine tolerance concedes a predictable share of queries to an attacker who controls the vectors: the hijack rate equals the distribution of angular retrieval margins at the tolerance (the margin law). Margins are small in five corpora and two embedding models, so an idealised tolerance at the level of floating-point noise leaves up to 5.5% of queries exposed (at most 1.2% in any corpus once exact duplicate documents are excluded), and a threshold calibrated from our CPU INT8-FP32 comparison of a small embedding model (at the empirical 0.1% quantile of honest cosines) leaves 98-100% exposed; on a Raspberry Pi 5 running a local language model, such an attack lowers correct answers from 0.75 to 0.39. Integrity audits of compressed vector stores fare no better: on a FAISS product-quantisation index over 57,638 documents, tampered vectors that all pass the audit put the attacker's document first for 25% of targets. Verifying quantisation codes instead, with ambiguity decided by the verifier, a calibrated guard band and canonicalisation, accepted every honest vector in our samples on three platforms and left the publisher no choice. We also show that common floating-point and dynamic-INT8 inference pipelines are not bit-reproducible across batch sizes or architectures, and report pre-registered negative results on abstention, context pruning and semantic screening. We release code and data.

*Özet kaynağı: arxiv:2611.06498 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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

- arXiv: https://arxiv.org/abs/2611.06498
- Metadata kaynakları: arxiv:2611.06498 (toplama: 2026-11-06)
