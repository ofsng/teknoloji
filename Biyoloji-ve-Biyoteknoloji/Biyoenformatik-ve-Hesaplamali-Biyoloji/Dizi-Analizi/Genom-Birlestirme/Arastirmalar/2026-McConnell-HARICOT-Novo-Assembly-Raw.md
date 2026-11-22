---
research_id: doi:10.64898/2026.11.11.765872
title: "HARICOT: De Novo Assembly of Raw Nanopore Signals using Fuzzy de Bruijn Graphs"
authors: ["Ulysse McConnell", "Quang Ngo", "Can Fırtına"]
year: 2026
published_date: 2026-11-18
updated_date: 2026-11-21
doi: 10.64898/2026.11.11.765872
arxiv:
url: https://doi.org/10.64898/2026.11.11.765872
publication: "bioRxiv (Cold Spring Harbor Laboratory)"
publication_type: preprint
peer_reviewed: false
primary_technology: genome-assembly
related_technologies: []
classification_confidence: high
classification_method: deterministic
keywords: ["nanopore sequencing", "de Bruijn graph", "Hough transform", "overlap detection", "genome assembly", "base calling", "assembly contiguity"]
source_ids: ["openalex:W7236449262"]
cited_by_count: 0
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

# HARICOT: De Novo Assembly of Raw Nanopore Signals using Fuzzy de Bruijn Graphs

## 1. Araştırmanın özeti

> Nanopore sequencing enables reading long nucleotide sequences by measuring characteristic changes in ionic current as molecules pass through a nanopore. These current measurements, known as raw signals, can be analyzed without translating them into bases (i.e., without basecalling), which provides fast and resource-efficient genome analysis. Prior work, Rawsamble, enables finding overlaps between raw nanopore signals, without basecalling them, and generating assemblies from these overlaps with off-the-shelf assemblers such as miniasm. Constructing assemblies directly from raw signals can substantially reduce redundancy and fragmentation in signal datasets, which is useful for many downstream tasks such as constructing non-redundant and accurate basecalled reads from assembled signals. However, existing overlap-based signal assembly strategies suffer from limited scalability and resolution mainly due to using off-the-shelf assemblers (e.g., miniasm) that are designed for basecalled sequences. While scalability and performance limitations can be addressed by existing de Bruijn graph approaches to assembly, their reliance on exact matches makes these methods too sensitive to the inherently noisy raw nanopore signals. To improve assembly of raw signals using de Bruijn graph approaches, we present HARICOT, a mechanism that constructs assemblies from raw nanopore signals by utilizing fuzzy de Bruijn graphs and Hough-transform-based overlap detection to robustly tolerate errors and noise in raw nanopore signals. Our evaluations on various genomes of different sizes show that HARICOT significantly improves assembly contiguity and quality compared to Rawsamble, helping close the gap to popular assembly tools such as Flye or wtdbg2 operating on nucleotide sequences. At the same time, performance remains comparable to these assemblers, without requiring additional basecalling. We discuss that assembling raw nanopore signals before basecalling enables future work in various ways such as building these de Bruijn graphs in a streaming way and assembly-aware basecalling techniques that can basecall assembly graphs for accurate and redundancy-resolved basecalling. HARICOT is available at https://github.com/STORMgroup/HARICOT . We also provide the scripts to fully reproduce our results on our GitHub page.

*Özet kaynağı: openalex:W7236449262 — lisans: cc-by. Tam metin incelenmedi.*

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
- **Kanonik konum:** [Genom Birleştirme](../_index.md)
<!-- AUTO:TECH:END -->

## 8. İlişkili araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

## 9. Kaynaklar

- DOI: https://doi.org/10.64898/2026.11.11.765872
- OpenAlex: https://openalex.org/W7236449262
- Metadata kaynakları: openalex:W7236449262 (toplama: 2026-11-21)
