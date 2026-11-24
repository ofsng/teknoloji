---
research_id: doi:10.1109/tifs.2026.3707794
title: "Scriptless Atomic Swap With Batch Processing"
authors: ["M M Wang", "Haotian Deng", "Mengxuan Liu", "Meng Li", "Chuan Zhang", "Licheng Wang", "Liehuang Zhu"]
year: 2026
published_date: 2026-01-01
updated_date: 2026-11-08
doi: 10.1109/tifs.2026.3707794
arxiv:
url: https://doi.org/10.1109/tifs.2026.3707794
publication: "IEEE Transactions on Information Forensics and Security"
publication_type: article
peer_reviewed: true
primary_technology: atomic-swaps
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["atomic swaps", "blockchain interoperability", "batch processing"]
source_ids: ["openalex:W7166064094"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-15
last_checked_at: 2026-11-15
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-24
---

# Scriptless Atomic Swap With Batch Processing

## 1. Araştırmanın özeti

> Cross-chain interoperability breaks down information silos between blockchains and enables the interconnection of blockchain systems. Atomic swap is a key technology of cross-chain interoperability that allows direct asset exchange between blockchains without intermediaries. Existing atomic swap schemes are typically based on hash time-locked contracts, which cannot be deployed on blockchains lacking scripting languages like Bitcoin. To eliminate reliance on scripting languages, Thyagarajan et al. proposed a scriptless atomic swap scheme, universal atomic swap [S&P’ 22], utilizing adaptor signature and verifiable timed discrete logarithm. However, its computational costs increase quadratically with the security parameter, and multiple rounds of communication are needed, resulting in low efficiency. Besides, when handling multi-asset swaps, delays in unlocking multiple assets can potentially result in asset losses and compromise fairness. In this paper, we propose SLAS, a scriptless atomic swap scheme with high computation and communication efficiency. Our fundamental design principle is to implement time lock and transaction lock off-chain using cryptographic tools while ensuring the capability to batch process multi-asset time locks. To achieve this goal, we first design verifiable timed key release (VTKR), a new cryptographic time-lock protocol, which can generate and verify time-lock for multiple assets simultaneously off-chain, such that both the locking and unlocking processes can be handled in a batch processing manner. Then, we introduce adaptor signature to generate transaction locks, ensuring the atomicity of transactions and reducing the communication overhead. We also perform both theoretical and experimental analysis, with results showing that SLAS is at least$792\times $faster for asset locking and$40\times $faster for transaction locking compared to existing schemes.

*Özet kaynağı: openalex:W7166064094 — lisans: cc-by. Tam metin incelenmedi.*

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

- DOI: https://doi.org/10.1109/tifs.2026.3707794
- OpenAlex: https://openalex.org/W7166064094
- Metadata kaynakları: openalex:W7166064094 (toplama: 2026-11-15)
