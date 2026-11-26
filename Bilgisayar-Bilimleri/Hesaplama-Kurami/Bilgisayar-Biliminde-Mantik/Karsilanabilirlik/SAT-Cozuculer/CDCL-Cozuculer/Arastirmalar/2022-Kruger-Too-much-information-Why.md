---
research_id: doi:10.1371/journal.pone.0272967
title: "Too much information: Why CDCL solvers need to forget learned clauses"
authors: ["Tom Krüger", "Jan-Hendrik Lorenz", "Florian Wörz"]
year: 2022
published_date: 2022-08-26
updated_date: 2026-11-23
doi: 10.1371/journal.pone.0272967
arxiv: 2202.01030
url: https://doi.org/10.1371/journal.pone.0272967
publication: "PLoS ONE"
publication_type: article
peer_reviewed: true
primary_technology: cdcl-solvers
related_technologies: []
classification_confidence: high
classification_method: "deterministic+backfill-explain"
keywords: ["conflict-driven clause learning", "SAT solvers", "clause learning", "clause deletion", "runtime distribution", "multimodal distributions", "unit propagation", "propositional satisfiability"]
source_ids: ["openalex:W4283220697"]
cited_by_count: 9
content_status: abstract_only
abstract_license: cc-by
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-23
last_checked_at: 2026-11-23
content_verified: false
identifier_verified: crossref
retraction_checked: 2026-11-26
---

# Too much information: Why CDCL solvers need to forget learned clauses

## 1. Araştırmanın özeti

> Conflict-driven clause learning (CDCL) is a remarkably successful paradigm for solving the satisfiability problem of propositional logic. Instead of a simple depth-first backtracking approach, this kind of solver learns the reason behind occurring conflicts in the form of additional clauses. However, despite the enormous success of CDCL solvers, there is still only a limited understanding of what influences the performance of these solvers in what way. Considering different measures, this paper demonstrates, quite surprisingly, that clause learning (without being able to get rid of some clauses) can not only help the solver but can oftentimes deteriorate the solution process dramatically. By conducting extensive empirical analysis, we furthermore find that the runtime distributions of CDCL solvers are multimodal. This multimodality can be seen as a reason for the deterioration phenomenon described above. Simultaneously, it also gives an indication of why clause learning in combination with clause deletion is virtually the de facto standard of SAT solving, in spite of this phenomenon. As a final contribution, we show that Weibull mixture distributions can accurately describe the multimodal distributions. Thus, adding new clauses to a base instance has an inherent effect of making runtimes long-tailed. This insight provides an explanation as to why the technique of forgetting clauses is useful in CDCL solvers apart from the optimization of unit propagation speed.

*Özet kaynağı: openalex:W4283220697 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [CDCL Çözücüler](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.1371/journal.pone.0272967
- arXiv: https://arxiv.org/abs/2202.01030
- OpenAlex: https://openalex.org/W4283220697
- Metadata kaynakları: openalex:W4283220697 (toplama: 2026-11-23)
