---
research_id: doi:10.47577/technium.v31i.13874
title: "Benchmarking Extended and Unscented Kalman Filters for Lithium-Ion Battery State-of-Charge Estimation against a Physics-Based Virtual Cell: Effects of OCV Flatness, Initial Covariance and Temperature"
authors: ["Zaid Ali", "Ihab A. Satam"]
year: 2026
published_date: 2026-11-03
updated_date: 2026-11-05
doi: 10.47577/technium.v31i.13874
arxiv:
url: https://doi.org/10.47577/technium.v31i.13874
publication: "Technium Romanian Journal of Applied Sciences and Technology"
publication_type: article
peer_reviewed: true
primary_technology: extended-and-unscented-kalman-filters
related_technologies: ["lithium-ion-batteries"]
classification_confidence: high
classification_method: deterministic
keywords: ["lithium-ion batteries", "state of charge estimation", "extended Kalman filter", "unscented Kalman filter", "Coulomb counting", "Virtual Cell", "Doyle-Fuller-Newman model", "equivalent circuit model", "temperature effects", "battery degradation", "convergence time", "Monte Carlo simulation"]
source_ids: ["openalex:W7225143559"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-20
last_checked_at: 2026-11-20
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-20
---

# Benchmarking Extended and Unscented Kalman Filters for Lithium-Ion Battery State-of-Charge Estimation against a Physics-Based Virtual Cell: Effects of OCV Flatness, Initial Covariance and Temperature

## 1. Araştırmanın özeti

> Kalman-filter state-of-charge (SoC) estimators are usually compared in simulations where the same equivalent circuit model (ECM) generates the data and runs inside the filter, and where errors are computed after the measurement update. Both practices flatter the estimators. This paper benchmarks Coulomb counting (CC), the extended Kalman filter (EKF) and the unscented Kalman filter (UKF) against a physics-based virtual cell: an experimentally parameterised Doyle–Fuller–Newman model of a 5 Ah LG M50 21700 cell with lumped thermal dynamics. A second-order RC ECM is identified from a simulated GITT/HPPC test (2.7 mV RMS fitting error) and then used, unchanged, by all estimators. The cell is driven by repeated UDDS and US06 cycles from 90 % to 10 % SoC at 10, 25 and 40 °C and in an aged state, with 10 mV voltage noise, 25 mA current noise and a 50 mA current offset. Errors are computed from the a priori estimate so that the initial error is always counted. With a correct initial SoC, both filters keep the RMSE between 0.39 % and 0.68 %, while CC drifts to 6.7 % over a 6.9 h UDDS test. A 300-run Monte Carlo study without SoC-limit effects shows that the two filters converge equally fast from under-estimated starts, but the EKF is markedly slower from over-estimated starts: with the recommended initial covariance its mean convergence time into a ±3 % band was 166 s (maximum 1110 s) against 1.2 s (maximum 2 s) for the UKF. All slow EKF runs started between 84 % and 93 % SoC, where the OCV slope of the cell falls to about 0.25 V per unit SoC; the EKF linearises at this flat point and applies too small a correction, whereas the UKF sigma points sample the steeper neighbouring regions. An initial covariance that is too small slows both filters by up to two orders of magnitude. At 10 °C, an ECM identified at 25 °C biases both filters by about −1 % to −2.5 %, which no filter tuning removes. The UKF costs about twice the computation of the EKF. The results show when the UKF is actually worth its cost and how the OCV shape of the specific cell should guide that choice.

*Özet kaynağı: openalex:W7225143559 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Genişletilmiş ve Kokusuz Kalman Filtreleri](../_index.md)
- **İlişkili:** [Lityum-İyon Bataryalar](../../../../../../../Enerji-Teknolojileri/Enerji-Depolama/Elektrokimyasal-Enerji-Depolama/Lityum-Iyon-Bataryalar/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.47577/technium.v31i.13874
- OpenAlex: https://openalex.org/W7225143559
- Metadata kaynakları: openalex:W7225143559 (toplama: 2026-11-20)
