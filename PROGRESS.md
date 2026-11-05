# İlerleme Durumu

Çalışma kesilirse buradan devam edin.

## v1 — Taksonomi (2026-11-05)

30 ana disiplin, 3492 düğüm; `tools/seed/*.tax`, `tools/kb.py`. Ayrıntı: TAXONOMY.md, SOURCES.md.

## v2 — Otonom araştırma sistemi (2026-11-05)

| Aşama | Durum | Not |
|---|---|---|
| 1. Mevcut sistemin doğrulanması | Tamam | `kb.py check` 0 hata. Bulunan ve düzeltilen hata: ilk kurulumda takma adlar `/` karakterinden bölünmüştü (ör. "PET/CT" → "PET","CT"); 7 düğüm onarıldı. "Data parallelism" takma adı mevcut "Veri Paralelliği" düğümüyle çakışıyordu, kaldırıldı. |
| Düzen geçişi | Tamam | 3492 `_index.md` 14 bölümlü 2. düzene, 3 araştırma dosyası yeni ön bilgiye taşındı; kimlik ve yollar değişmedi (karşılaştırmalı doğrulandı). |
| 2. Toplama | Tamam | arXiv + OpenAlex (dergi/konferans, bioRxiv/medRxiv) + Crossref. Gerçek çalışma: 3.867 kayıt tarandı, 38 arşivlendi. |
| 3. Sınıflandırma | Tamam | Etiketli setle ölçüldü: `high` doğru dal 0,94 (n=33). Üretim örneği 34/38. |
| 4. Markdown arşivi | Tamam | Tekilleştirme, sürüm birleştirme, kimlik doğrulama (Crossref/doi.org), geri çekme denetimi. |
| 5. Teknoloji keşfi | Tamam (kanıt birikiyor) | İlk günde aday yok (eşik: 5 makale, 3 yazar, 2 ay). 258 terim izleniyor. |
| 6. Teknoloji açıklamaları | Pilot | 2 düğüm kaynaklı dolduruldu (`ai_draft_sourced`): kuantum hata düzeltme, sıfır bilgi ispatları. Otomatik doldurma LLM anahtarı gerektirir. |
| 7. Otomasyon | Bkz. aşağı | `.github/workflows/daily-research.yml` |

## Açık işler

- [ ] GitHub'da `OPENALEX_API_KEY` (ücretsiz) ve isteğe bağlı `ANTHROPIC_API_KEY` gizli değerlerini tanımlamak.
- [ ] Depo ayarı: "Allow GitHub Actions to create and approve pull requests" (kapalıysa iş akışı yalnızca dalı gönderir).
- [ ] `review/CLASSIFICATION-QUEUE.md` ve aday listesini düzenli gözden geçirmek.
- [ ] Pilot `_index.md` içeriklerini (2 düğüm) okuyup onaylamak (`content_status: human_verified`, `content_verified: true`).
- [ ] Değerlendirme setini insan etiketleriyle genişletmek (şu an 70 kayıt, Claude etiketli).
- [ ] Tarihsel tamamlamada düğüm adı başlıkta geçmeyen temel çalışmalar (ör. "Attention Is All You Need") kaçırılıyor; takma adlarla arama eklenebilir.
- [ ] Önceki taksonomi açık işleri (ACM CCS/MeSH/IEEE karşılaştırmaları, sığ disiplinler).

## Devam etme komutları

```bash
cd Technology-Knowledge-Base
python3 tools/autokb.py status
python3 -m unittest discover -s tools/tests
python3 tools/kb.py check
```
