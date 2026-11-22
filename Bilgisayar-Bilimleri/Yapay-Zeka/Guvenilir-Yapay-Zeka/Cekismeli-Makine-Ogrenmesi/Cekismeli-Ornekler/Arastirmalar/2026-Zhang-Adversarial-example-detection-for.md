---
research_id: doi:10.3389/fcomp.2026.1897185
title: "Adversarial example detection for image captioning models via SPC-verify"
authors: ["Dehai Zhang", "Jiaqi Mao", "Jiajun Zhu"]
year: 2026
published_date: 2026-11-04
updated_date: 2026-11-21
doi: 10.3389/fcomp.2026.1897185
arxiv:
url: https://doi.org/10.3389/fcomp.2026.1897185
publication: "Frontiers in Computer Science"
publication_type: article
peer_reviewed: true
primary_technology: adversarial-examples
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["adversarial example detection", "image captioning", "BLIP", "counterfactual reasoning"]
source_ids: ["openalex:W7225257522"]
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

# Adversarial example detection for image captioning models via SPC-verify

## 1. Araştırmanın özeti

> Image captioning models are vulnerable to adversarial examples that can induce descriptions inconsistent with visual evidence, commonsense knowledge, or physical rules. Existing detection methods mainly rely on confidence anomalies, feature-space deviations, or reconstruction errors, making them less suitable for cross-modal generative tasks. To address this limitation, we propose SPC-Verify, a Semantic-Phenomenon Consistency Verification framework for adversarial example detection in image captioning. The framework combines Visual-Semantic Consistency Verification (VSCV), which assesses whether token-level visual evidence supports the corresponding generated concepts, with Phenomenon Plausibility Verification (PPV), which evaluates the consistency of complete captions with commonsense knowledge and physical constraints. To improve the reliability of local visual evidence, we introduce SCAR-SAT, a post-hoc heatmap refinement method for Show-Attend-and-Tell-based models that integrates semantic consistency, lightweight counterfactual support, spatial continuity, and temporal stability. We further propose Zero-Shot Cross-Model Threshold Transfer (ZS-CMTT), which learns shared decision thresholds from the joint score distributions of SAT and BLIP and transfers them to unseen captioning models without requiring target-model samples. Experiments on MSCOCO and Flickr30K across SAT and BLIP, under multiple attack settings, demonstrate the effectiveness of the proposed framework. Ablation studies show that the Grounded Category Vocabulary improves token-level verification, while PPV provides complementary sentence-level plausibility assessment. Further evaluations indicate that SCAR-SAT improves token-level visual grounding and that ZS-CMTT facilitates threshold transfer across captioning models. Overall, SPC-Verify provides an interpretable and transferable approach to adversarial example detection by jointly evaluating local visual-semantic consistency and global caption plausibility.

*Özet kaynağı: openalex:W7225257522 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Çekişmeli Örnekler](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3389/fcomp.2026.1897185
- OpenAlex: https://openalex.org/W7225257522
- Metadata kaynakları: openalex:W7225257522 (toplama: 2026-11-22)
