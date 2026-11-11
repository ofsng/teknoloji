---
research_id: doi:10.21067/smartics.v12i2.14779
title: "Anomali Deteksi Log Trafic Sistem Keamanan Jaringan Menggunakan Intrusion Detection System (Ids) Berbasis Snort Pada Web Server"
authors: ["Wahyu Eko Febrianto", "Ahmad Zulham Fahamsyah Havy", "Muhammad Faishol Amrulloh"]
year: 2026
published_date: 2026-11-02
updated_date: 2026-11-06
doi: 10.21067/smartics.v12i2.14779
arxiv:
url: https://doi.org/10.21067/smartics.v12i2.14779
publication: "SMARTICS Journal"
publication_type: article
peer_reviewed: true
primary_technology: intrusion-detection-systems
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["intrusion detection systems", "Snort", "UDP flood attacks", "DDoS attacks", "DDoS mitigation", "web server security"]
source_ids: ["openalex:W7225236010"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by-sa
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-10
last_checked_at: 2026-11-10
content_verified: false
identifier_verified: not_found
retraction_checked: 2026-11-10
---

# Anomali Deteksi Log Trafic Sistem Keamanan Jaringan Menggunakan Intrusion Detection System (Ids) Berbasis Snort Pada Web Server

## 1. Araştırmanın özeti

> One threat that can disrupt service availability is the Distributed Denial of Service (DDoS) attack—specifically UDP Flood attacks—which can cause bandwidth saturation. This study aims to analyze abnormal traffic patterns on a web server and implement a Snort-based Intrusion Detection System (IDS) alongside a mitigation mechanism using the RAW Firewall on a MikroTik Cloud Core Router (CCR). A quantitative approach was employed, utilizing traffic and network log analysis to identify attack characteristics, including protocols, source and destination addresses, service ports, packet sizes, and packet transmission patterns. Analysis revealed relatively small UDP packets being repeatedly sent from multiple source IP addresses to port 53 (DNS) at high frequency, indicating UDP Flood/DDoS activity. Prior to mitigation, inbound traffic averaged 207.94 Mbps with a peak of 306.20 Mbps , whereas the available bandwidth capacity was only 100 Mbps . This situation caused bandwidth saturation and negatively impacted web server service quality. Mitigation was achieved by applying a RAW Firewall rule on the MikroTik CCR to drop UDP packets destined for port 53 during the *prerouting* stage. Following mitigation, inbound traffic dropped to an average of 43.21 Mbps with a peak of 60.72 Mbps . Consequently, peak traffic decreased by approximately 80.17% , returning to a level below the 100 Mbps bandwidth capacity. The results demonstrate that combining Snort IDS for detection and the MikroTik RAW Firewall for mitigation effectively reduces the impact of UDP Flood/DDoS attacks while enhancing the stability and availability of web server services.

*Özet kaynağı: openalex:W7225236010 — lisans: cc-by-sa. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Saldırı Tespit Sistemleri](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.21067/smartics.v12i2.14779
- OpenAlex: https://openalex.org/W7225236010
- Metadata kaynakları: openalex:W7225236010 (toplama: 2026-11-10)
