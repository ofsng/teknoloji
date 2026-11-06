---
research_id: arxiv:2611.06502
title: "A Variational Quantum Algorithm for Multi-Skill Project Scheduling"
authors: ["Raul Martinez", "Miguel Sánchez-Beato", "Matilde Osa", "Jorge Parra", "Mario Calonge"]
year: 2026
published_date: 2026-11-04
updated_date: 2026-11-04
doi:
arxiv: 2611.06502
url: https://arxiv.org/abs/2611.06502
publication: arXiv
publication_type: preprint
peer_reviewed: false
primary_technology: variational-quantum-algorithms
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: []
source_ids: ["arxiv:2611.06502"]
cited_by_count:
content_status: abstract_only
abstract_license: "cc0-1.0 (arxiv metadata)"
retraction_status: none_reported
related_versions: []
collected_at: 2026-11-06
last_checked_at: 2026-11-06
content_verified: false
identifier_verified: arxiv
---

# A Variational Quantum Algorithm for Multi-Skill Project Scheduling

## 1. Araştırmanın özeti

> Job scheduling is an NP-hard optimization problem with clear industrial relevance. In practice, distributing work across a team is not only about meeting deadlines or improving productivity; it also affects fatigue, stress, and employee well-being. Variational Quantum Algorithms (VQAs) provide a promising way to address these problems through QUBO formulations, although their scalability on near-term NISQ hardware is still limited by Hilbert-space growth and barren plateaus. In this work, we simulate a VQA for a realistic Multi-Skill Resource-Constrained Project Scheduling Problem (MS-RCPSP), including worker capacities, skill matrices, task priorities, deadlines, and calendar stability during rescheduling. To keep the problem within a near-term circuit size, we use a temporal batch decomposition that solves one day at a time, propagates the remaining workload, and combines it with a logarithmic binary encoding that keeps every batch at or below 30 qubits. Because the ground state of a QUBO Hamiltonian is a computational basis state, entanglement is not required to represent the solution, raising the question of whether it helps or hinders ansatz training. We address this question by comparing the linear and brick-wall entangling topologies of a hardware-efficient ansatz with an entanglement-free reference that has the same number of parameters and by training every configuration with COBYLA and with Adam using SPSA gradient estimation. For the instance and initialization studied, the entanglement-free reference produced feasible schedules under both optimizers. With COBYLA, it produced the feasible schedule closest to the required workload at a fraction of the simulation cost of the entangled topologies, indicating that entanglement did not improve the solutions found by the VQA.

*Özet kaynağı: arxiv:2611.06502 — lisans: cc0-1.0 (arxiv metadata). Tam metin incelenmedi.*

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
- **Kanonik konum:** [Varyasyonel Kuantum Algoritmaları](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- arXiv: https://arxiv.org/abs/2611.06502
- Metadata kaynakları: arxiv:2611.06502 (toplama: 2026-11-06)
