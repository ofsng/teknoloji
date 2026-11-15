---
research_id: doi:10.1613/jair.1.22089
title: "BCAT: A Block Causal Transformer for PDE Foundation Models for Fluid Dynamics"
authors: ["Yuxuan Liu", "Jingmin Sun", "Hayden Schaeffer"]
year: 2026
published_date: 2026-11-11
updated_date: 2026-11-13
doi: 10.1613/jair.1.22089
arxiv: 2501.18972
url: https://doi.org/10.1613/jair.1.22089
publication: "Journal of Artificial Intelligence Research"
publication_type: article
peer_reviewed: true
primary_technology: fluid-dynamics
related_technologies: ["foundation-models"]
classification_confidence: high
classification_method: deterministic
keywords: ["partial differential equations", "fluid dynamics", "foundation models", "autoregressive forecasting", "next-frame prediction", "spatiotemporal dependencies", "physics-informed neural networks", "Muon optimizer"]
source_ids: ["openalex:W4407093477"]
cited_by_count: 21
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-14
last_checked_at: 2026-11-14
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-14
---

# BCAT: A Block Causal Transformer for PDE Foundation Models for Fluid Dynamics

## 1. Araştırmanın özeti

> Background: Foundation models have demonstrated remarkable generalization in vision and language, but their accurate use for scientific computing remains challenging. For two-dimensional fluid-dynamics prediction, current transformer-based models are often hindered by limited context and rigid causality information, as they typically map fixed windows to the next step. Objectives: We aim to develop a unified architecture for heterogeneous fluid-dynamics families. The goal is to better capture the complex spatio-temporal dependencies inherent in nonlinear fluid dynamics. Methods: We introduce BCAT, a block-causal transformer for autoregressive prediction of two-dimensional fluid-dynamics solutions. Our approach adapts block-causal attention to next-frame prediction, leveraging previous frames as contextual priors. The model is trained on 69K trajectory sequences from PDEBench, PDEArena, and CFDBench using the Muon optimizer. Results: BCAT achieved an average relative 𝐿 2 error of 1.18% across the six evaluated fluid families, reducing error by 45% relative to a 3.4-times-larger baseline. In ablations, next-frame prediction was 3.5x more accurate than the corresponding nexttoken variant. A five-seed analysis, noisy-input stress test, long-rollout analysis, and physics diagnostics further characterize the model. Conclusions: The block-causal framework captures spatial interactions within frames while enforcing temporal causality across frames. BCAT provides an accurate and computationally efficient model for the two-dimensional fluid-dynamics benchmarks considered here.

*Özet kaynağı: openalex:W4407093477 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Akışkanlar Dinamiği](../_index.md)
- **İlişkili:** [Temel Modeller](../../../Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Temel-Modeller/_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1613/jair.1.22089
- arXiv: https://arxiv.org/abs/2501.18972
- OpenAlex: https://openalex.org/W4407093477
- Metadata kaynakları: openalex:W4407093477 (toplama: 2026-11-14)
