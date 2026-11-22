---
research_id: doi:10.1145/3864457
title: "Direction-Aware Timing Modeling for Reinforcement-Learning-Based Clock Arrival Time Optimization in Power-Integrity-Aware Physical Design"
authors: ["Cankun HUANG", "Jiangxia Deng", "Hailuan Liu", "Guorui Feng", "Lingyan Fan"]
year: 2026
published_date: 2026-11-19
updated_date: 2026-11-21
doi: 10.1145/3864457
arxiv:
url: https://doi.org/10.1145/3864457
publication: "ACM Transactions on Design Automation of Electronic Systems"
publication_type: article
peer_reviewed: true
primary_technology: power-integrity
related_technologies: ["physical-design", "reinforcement-learning"]
classification_confidence: high
classification_method: deterministic
keywords: ["power integrity", "reinforcement learning", "clock skew", "timing margin", "peak current reduction"]
source_ids: ["openalex:W7236652213"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-22
last_checked_at: 2026-11-22
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-22
---

# Direction-Aware Timing Modeling for Reinforcement-Learning-Based Clock Arrival Time Optimization in Power-Integrity-Aware Physical Design

## 1. Araştırmanın özeti

> Dynamic IR-drop induced by large-scale synchronous register switching has become a critical power-integrity challenge in modern high-performance ICs. Highly balanced clock networks can trigger simultaneous switching, causing transient current surges, localized voltage drops, timing-margin loss, and potential functional failures. Existing clock-skew and Clock Arrival Time (CAT) optimization methods mitigate this issue by expanding CAT distributions to desynchronize register switching, but recent reinforcement-learning-based approaches often rely on aggregated TNS-only timing observations, which obscure the directional timing impact of CAT perturbations. This work proposes Direction-Aware Timing Modeling (DATM) for reinforcement-learning-based CAT optimization. DATM explicitly separates launch-side and capture-side timing behaviors, resolving the directional ambiguity of TNS-only formulations and enabling the agent to better infer how CAT adjustments affect timing. The proposed framework is evaluated on seven 28nm designs with diverse timing and structural characteristics. Results show that DATM achieves substantially larger CAT-distribution expansion than the evaluated baselines while maintaining stable setup timing. A comprehensive timing-surrogate audit quantifies model fidelity, and CAT-transfer analysis shows that physical implementation preserves CAT ordering while attenuating target amplitude. Industrial validation with ICC2 and RedHawk further demonstrates an average peak-current reduction of 50.57% and dynamic IR-drop hotspot reduction, with limited timing degradation and average total-area and total-power overheads of 9.33% and 8.63%, respectively. These results establish DATM as a practical EDA method for power-integrity-aware physical design.

*Özet kaynağı: openalex:W7236652213 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Güç Bütünlüğü](../_index.md)
- **İlişkili:** [Fiziksel Tasarım](../../../../Entegre-Devre-Tasarimi/Sayisal-Entegre-Devre-Tasarimi/Fiziksel-Tasarim/_index.md), [Pekiştirmeli Öğrenme](../../../../../Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Pekistirmeli-Ogrenme/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1145/3864457
- OpenAlex: https://openalex.org/W7236652213
- Metadata kaynakları: openalex:W7236652213 (toplama: 2026-11-22)
