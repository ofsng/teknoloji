---
research_id: doi:10.3390/electronics15215097
title: "Reducing Test Response Volume and Test Time in Direct-Access-Based High-Bandwidth Memory Testing"
authors: ["Jawon Koo", "Eunki Kim", "Hankyu Lee", "Han-Bin Lee", "Dongsup Song"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-05
doi: 10.3390/electronics15215097
arxiv:
url: https://doi.org/10.3390/electronics15215097
publication: Electronics
publication_type: article
peer_reviewed: true
primary_technology: high-bandwidth-memory
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["high-bandwidth memory", "test time reduction", "HBM2"]
source_ids: ["openalex:W7225180152"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-12
last_checked_at: 2026-11-12
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-12
---

# Reducing Test Response Volume and Test Time in Direct-Access-Based High-Bandwidth Memory Testing

## 1. Araştırmanın özeti

> In high-bandwidth memory (HBM) testing through the direct access (DA) port, the response-path bandwidth is far lower than the internal data bandwidth. Because most read responses are fault-free, transferring every response incurs substantial transfer overhead and test time. This paper proposes three fault-data transfer methods. Selective staggered read suppresses fault-free response transfers and overlaps faulty-response transfers with the subsequent read latency. Duplicate fault suppression replaces identical fault responses at consecutive addresses with a short duplicate code. Failing-bit indexing transmits only the positions of failing bits. The proposed architecture controls whether, when, and in which format each response is transferred without modifying the DA port interface or the March command and address sequence. Cycle-accurate simulation of an HBM2 test model shows that, across Random, Column-Correlated, and Row-Correlated Fault models with fault rates of 0.01–5%, the proposed method reduces the DA response data by 99.32–99.99% and the total test time by 44.86–45.01% compared with the conventional method. Synthesis shows that the added logic is smaller than that of on-chip fault collection and signature compaction schemes and independent of the memory capacity. The proposed architecture attains nearly the same test time as on-chip fault collection and signature compaction schemes while delivering every faulty response and its failing-bit positions to the tester, so that its diagnostic coverage is not bounded by on-chip storage.

*Özet kaynağı: openalex:W7225180152 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Yüksek Bant Genişlikli Bellek](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/electronics15215097
- OpenAlex: https://openalex.org/W7225180152
- Metadata kaynakları: openalex:W7225180152 (toplama: 2026-11-12)
