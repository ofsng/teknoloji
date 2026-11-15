---
research_id: doi:10.62056/abe0ivol7
title: "Atomic Swaps with Relaxed Assumptions"
authors: ["Paul Rösler", "Katharina Schambach", "Julian Thomas"]
year: 2026
published_date: 2026-05-04
updated_date: 2026-11-10
doi: 10.62056/abe0ivol7
arxiv:
url: https://doi.org/10.62056/abe0ivol7
publication: "IACR Communications in Cryptology"
publication_type: article
peer_reviewed: true
primary_technology: atomic-swaps
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["atomic swaps", "blockchain interoperability", "deadlock prevention", "unlinkability", "fungibility", "universal composability", "privacy preservation"]
source_ids: ["openalex:W7160195045"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-15
last_checked_at: 2026-11-15
content_verified: false
identifier_verified: false
---

# Atomic Swaps with Relaxed Assumptions

## 1. Araştırmanın özeti

> Atomic swaps allow two parties to exchange coins across blockchains without trust. Most existing solutions support a 1-to-1 transaction; however, the value ratio of two cryptocurrencies is usually not 1-to-1. In addition, these solutions often rely on blockchains with explicit support structures for atomic swaps, typically hashed timelocks (HTLCs) or smart-contract scripting. Thyagarajan et al. (SP'22) provide a solution for n-to-m swaps utilizing adaptor signatures instead, which offer better privacy for the participants. Significantly, all these approaches need timed transactions or a similar substitute on both sides, but not every blockchain supports timed transactions. Hoenisch et al. (ESORICS'22) demonstrate a concrete swap procedure between Bitcoin and Monero, where only one side needs timed transactions. We build upon both of these ideas to provide a generic solution for any blockchain, where only one side needs timed transactions. We introduce a generic adaptor-signature protocol for n-to-m swaps. In doing so, we minimize assumptions compared to current solutions. Both sides lock their coins in shared (two-party signature) addresses, where they can only access the coins together. To prevent deadlocks, both parties are able to refund their coins from these addresses with pre-signed transactions. Our solution works with all relevant blockchains because it needs only standard signatures and a joint public key. Further, only one side needs timed transactions, and if each party acts in its best interest, there are two possible outcomes: If progress stalls, the side with timelocks refunds after a certain time, and the other side refunds immediately. Otherwise, one party redeems the other party's coins with pre-signed transactions, and the other party completes the swap after a timeout to prevent race conditions. We prove security in the universal composability framework and show privacy preservation via unlinkability and fungibility.

*Özet kaynağı: openalex:W7160195045 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Atomik Takaslar](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.62056/abe0ivol7
- OpenAlex: https://openalex.org/W7160195045
- Metadata kaynakları: openalex:W7160195045 (toplama: 2026-11-15)
