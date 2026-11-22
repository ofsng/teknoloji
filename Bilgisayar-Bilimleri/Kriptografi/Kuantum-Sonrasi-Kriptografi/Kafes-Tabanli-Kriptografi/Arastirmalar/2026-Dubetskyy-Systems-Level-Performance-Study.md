---
research_id: doi:10.3390/info17111098
title: "A Systems-Level Performance Study of Post-Quantum TLS with ML-KEM and ML-DSA in Modern OpenSSL"
authors: ["Volodymyr Dubetskyy", "Maria‐Dolores Cano"]
year: 2026
published_date: 2026-11-04
updated_date: 2026-11-16
doi: 10.3390/info17111098
arxiv:
url: https://doi.org/10.3390/info17111098
publication: Information
publication_type: article
peer_reviewed: true
primary_technology: lattice-based-cryptography
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["post-quantum cryptography", "TLS 1.3", "ML-KEM", "ML-DSA", "OpenSSL", "X25519", "time to first byte", "packetization", "packet loss", "TCP connection establishment", "performance evaluation"]
source_ids: ["openalex:W7225245685"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-18
last_checked_at: 2026-11-18
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-18
---

# A Systems-Level Performance Study of Post-Quantum TLS with ML-KEM and ML-DSA in Modern OpenSSL

## 1. Araştırmanın özeti

> Large-scale quantum computers threaten the classical public-key foundations of Transport Layer Security (TLS), motivating deployment of standardized post-quantum cryptography (PQC). This study evaluates post-quantum TLS 1.3 as a systems-level deployment problem in OpenSSL 3.4.1 with the Open Quantum Safe provider and in OpenSSL 3.5.0 with native PQC support. We combine cryptographic microbenchmarks, TLS 1.3 connection timing, end-to-end HTTP time to first byte (TTFB), controlled network impairment, packetization analysis, and concurrency tests on two x86-64 systems, and release the measurement archive with the analysis scripts. For hybrid X25519MLKEM768, the median TTFB overhead relative to classical TLS was 6.5–7.5% with OpenSSL 3.4.1 and 1.2–1.3% with OpenSSL 3.5.0. These cross-release comparisons describe complete software configurations. In authentication-matched runs, replacing RSA-PSS with ML-DSA-65 changed median TTFB by −3.0 to +0.1 ms. The full-PQC configuration enlarged the server handshake flight from 1.3 kB to 10.1 kB, mainly through ML-DSA-65 authentication, and increased server-to-client payload segments from 4–5 to 11–13. At a round-trip time of 50 ms, 1% packet loss increased p99 TTFB 6–8-fold in all configurations. Most of this tail consisted of requests delayed by about 1 s, whose frequency matched the probability of losing a TCP connection-establishment segment and was similar for all configurations. Under concurrent load, OpenSSL 3.5.0 completed 46–58% more requests per second.

*Özet kaynağı: openalex:W7225245685 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Kafes Tabanlı Kriptografi](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/info17111098
- OpenAlex: https://openalex.org/W7225245685
- Metadata kaynakları: openalex:W7225245685 (toplama: 2026-11-18)
