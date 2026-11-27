---
research_id: doi:10.3390/a19121027
title: "ECoT: Explicit Chain-of-Thought Reasoning for Zero-Shot Composed Image Retrieval"
authors: ["Shanjie Xu", "Donglan Liu", "Yuhui Jin", "Honglei Yao", "Fuhui Zhao", "Hao Zhang", "Xin Liu"]
year: 2026
published_date: 2026-11-23
updated_date: 2026-11-26
doi: 10.3390/a19121027
arxiv:
url: https://doi.org/10.3390/a19121027
publication: Algorithms
publication_type: article
peer_reviewed: true
primary_technology: llm-reasoning-methods
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["composed image retrieval", "zero-shot retrieval", "chain-of-thought reasoning", "multimodal large language models", "rank fusion"]
source_ids: ["openalex:W7238790302"]
cited_by_count: 0
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-26
last_checked_at: 2026-11-26
content_verified: false
identifier_verified: crossref
---

# ECoT: Explicit Chain-of-Thought Reasoning for Zero-Shot Composed Image Retrieval

## 1. Araştırmanın özeti

> Composed Image Retrieval (CIR) aims to retrieve a target image using a query consisting of a reference image and a textual modification instruction. Recent CIR methods can be categorized as zero-shot and supervised methods. Typical zero-shot CIR studies commonly employ Multimodal Large Language Models (MLLMs) with Chain-of-Thought (CoT) prompting to generate target descriptions for retrieval. However, existing approaches still face several limitations: (1) Their retrieval-critical intermediate reasoning outcomes are often compressed into final descriptions rather than being explicitly preserved as retrieval evidence; (2) The generated descriptions in these studies may contain objective inconsistencies, while heterogeneous retrieval evidence cannot be reliably aggregated using raw similarity scores; and (3) Existing ranking strategies primarily rely on generated descriptions, without sufficiently exploiting the original reference image and modification instruction to distinguish fine-grained candidates. To address these limitations, we propose ECoT, an Explicit Chain-of-Thought reasoning framework that transforms retrieval-critical intermediate semantics into complementary retrieval evidence. Specifically, for Limitation 1, we introduce Explicit Dual-Path Reasoning, which constructs complementary target representations by generating multi-granularity descriptions and a minimal description containing only essential target semantics. For Limitation 2, Dual-Path Rank Fusion aggregates the rankings from different reasoning paths, while Objective Reflection and Correction serves as an auxiliary mechanism that checks for potential semantic inconsistencies and appends corrective queries when needed. Finally, for Limitation 3, Candidate-Level Semantic Calibration incorporates the fused base score, reference-image similarity, and instruction-image compatibility to refine candidate ranking. We evaluate ECoT on CIRR and CIRCO using the CLIP ViT-B/32 and ViT-L/14 encoder variants. With ViT-L/14, ECoT achieves Full and Subset Recall@1 of 38.00% and 72.07% on CIRR, improving over the strongest baseline by 6.19 and 4.86 percentage points, respectively, and achieves 25.44% mAP@5 on CIRCO. These results highlight ECoT's potential for interactive visual search and e-commerce retrieval, where distinguishing visually similar candidates according to user-specified modifications is essential, without task-specific neural network training. Fusion and calibration weights are selected using labeled validation data.

*Özet kaynağı: openalex:W7238790302 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [LLM Akıl Yürütme Yöntemleri](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.3390/a19121027
- OpenAlex: https://openalex.org/W7238790302
- Metadata kaynakları: openalex:W7238790302 (toplama: 2026-11-26)
