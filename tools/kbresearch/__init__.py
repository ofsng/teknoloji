"""Otonom araştırma toplama, sınıflandırma, teknoloji keşfi ve bilgi bakımı.

Bileşenler:
  sources/    Research Collector kaynak bağdaştırıcıları (arXiv, OpenAlex, Crossref)
  classify    Research Classifier (deterministik; isteğe bağlı LLM)
  archive     Araştırma Markdown arşivi (tekilleştirme, birleştirme)
  discovery   Technology Discovery (aday yönetimi)
  maintainer  Knowledge Maintainer (_index.md içerik doldurma ve güncelleme önerileri)
  pipeline    Günlük çalışma ve tarihsel tamamlama

Yalnızca standart kütüphane kullanır; `anthropic` paketi yalnızca LLM modu için gereklidir.
"""
