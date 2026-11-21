---
research_id: doi:10.1145/3802824
title: "Understanding the Fundamental Design Decisions of Retrieval-Augmented Generation Systems"
authors: ["Shengming Zhao", "Yuchen Shao", "Yuheng Huang", "Jiayang Song", "Zhijie Wang", "Chengcheng Wan", "Лей Ма"]
year: 2026
published_date: 2026-11-18
updated_date: 2026-11-20
doi: 10.1145/3802824
arxiv: 2411.19463
url: https://doi.org/10.1145/3802824
publication: "ACM Transactions on Software Engineering and Methodology"
publication_type: article
peer_reviewed: true
primary_technology: retrieval-augmented-generation
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["retrieval-augmented generation", "large language models", "knowledge integration", "prompting", "question answering", "code generation", "failure modes"]
source_ids: ["openalex:W4405030403"]
cited_by_count: 49
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-21
last_checked_at: 2026-11-21
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-21
---

# Understanding the Fundamental Design Decisions of Retrieval-Augmented Generation Systems

## 1. Araştırmanın özeti

> Retrieval-Augmented Generation (RAG) has emerged as a critical technique for enhancing large language model (LLM) capabilities. However, practitioners face significant challenges when making RAG deployment decisions. While existing research prioritizes algorithmic innovations, a systematic gap persists in understanding fundamental engineering tradeoffs that determine RAG success. We present the first comprehensive study of three universal RAG deployment decisions: whether to deploy RAG, how much information to retrieve, and how to integrate retrieved knowledge effectively. Through systematic experiments across three LLMs and six datasets spanning question answering and code generation tasks, we reveal critical insights: (1) RAG deployment must be highly selective, with variable recall thresholds and failure modes affecting up to 12.6% of samples even with perfect documents. (2) Optimal retrieval volume exhibits task-dependent behavior—QA tasks show universal patterns (5–10 documents optimal) while code generation requires scenario-specific optimization. (3) Knowledge integration effectiveness depends on task and model characteristics, with code generation benefiting significantly from prompting methods while question answering shows minimal improvement. These findings demonstrate that universal RAG strategies prove inadequate. Effective RAG systems require context-aware design decisions based on task characteristics and model capabilities. Our analysis provides evidence-based guidance for practitioners and establishes foundational insights for principled RAG deployment. Our code, data, and artifacts are publicly available at https://github.com/ShengmingZ/RAG_Benchmark_Code_QA .

*Özet kaynağı: openalex:W4405030403 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Erişimle Zenginleştirilmiş Üretim](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1145/3802824
- arXiv: https://arxiv.org/abs/2411.19463
- OpenAlex: https://openalex.org/W4405030403
- Metadata kaynakları: openalex:W4405030403 (toplama: 2026-11-21)
