# İlerleme Durumu

Çalışma kesilirse buradan devam edin.

## v1 — Taksonomi (2026-11-05)

30 ana disiplin, 3492 düğüm; `tools/seed/*.tax`, `tools/kb.py`. Ayrıntı: TAXONOMY.md, SOURCES.md.

## v2 — Otonom araştırma sistemi (2026-11-05)

Toplama (arXiv, OpenAlex, Crossref), sınıflandırma, arşiv, teknoloji keşfi, bilgi bakımı, günlük iş akışı.
Ayrıntı: AUTOMATION.md. Otomatik çalışmalar `auto/research` dalında birikir ve PR #1 üzerinden incelenir.

## v2.1 — Kayıp önleme, kalibrasyon, ücretsiz LLM (2026-11-07, PR #2)

| Konu | Durum |
|---|---|
| Araştırma kaybı | Düzeltildi. Eski sürüm bütçeye takılan yüksek güvenli kayıtları atıyordu (11-05: 561, 11-06: 518). Kalıcı backlog + defter; tek seferlik kurtarma gerçek bot durumunda denendi: 6 gün/akış yeniden tarandı, 1.085 kayıt backlog'a girdi, 40'ı arşivlendi (27'si ilk kez araştırma alan teknolojiler). |
| Geç dizinlenen yayınlar | OpenAlex yayın günü 10 ve 30 gün sonra yeniden taranır (yalnızca `created_date` yeni olanlar); arXiv 7 gün sonra. Anahtarla tam günlük kapsam (önceden günün ~%22'si). |
| Sınıflandırma | Kalibrasyon (90 kayıt): yüksek güven eşiği 6,0 → 7,5. Bağımsız sette arşive girenlerin kesinliği 0,94 → 1,00 (n=22). |
| İnceleme kuyruğu | Tekrar birleştirme, öncelik, 150 sınırı, 30 gün sonra deftere. |
| Teknoloji adayları | Çakışma kontrolü; eski "artificial neural network → ANN araması eş anlamlısı" kararı geri alındı; "multimodal large language model" LLM'in alt türü ve olası çakışma olarak işaretlendi. |
| Ücretsiz LLM | GitHub Models kapatılmış. Yerel llama.cpp + Qwen3-4B-Instruct-2507 Actions'ta doğrulandı; alıntı modu. Pilot: 9/10 düğüm, 22 denetlenmiş alıntı, kırık bağlantı yok. |
| Actions uyarıları | Node 20 uyarısı: checkout@v7, setup-python@v7, cache@v5, upload-artifact@v6 (Node 24). |
| Önceki açık işler | Tamamlandı: `OPENALEX_API_KEY` tanımlandı; Actions'ın PR açma izni verildi. |

## Açık işler

- [ ] PR #2'yi incelemek ve birleştirmek (birleşince günlük iş akışı kurtarmayı otomatik yapar).
- [ ] PR #1'deki birikmiş araştırmaları ve `review/` kuyruklarını gözden geçirmek.
- [ ] Alıntı modundaki bölümler için Türkçe özet: Gemini/Groq ücretsiz anahtarı (`KB_LLM_PROVIDER=openai`, `KB_LLM_TEXT_MODE=summary`) ya da insan.
- [ ] Yerel model için 8B sınıfı (ör. Qwen3-8B) Türkçe kalitesini denemek (2× yavaş).
- [ ] Pilot ve ilk iki `_index.md` içeriklerini okuyup onaylamak (`content_status: human_verified`, `content_verified: true`).
- [ ] Değerlendirme setlerini insan etiketleriyle genişletmek (şu an 70 + 90 kayıt, Claude etiketli).
- [ ] Backlog günde ~500 kayıt büyüyor, günde 40 arşivleniyor; sınır (3.000) aşılınca düşük öncelikliler deftere geçer. Bütçe ihtiyaca göre `KB_MAX_ARCHIVE_PER_RUN` ile ayarlanabilir.
- [ ] Tarihsel tamamlamada düğüm adı başlıkta geçmeyen temel çalışmalar kaçırılıyor (takma adlarla arama).

## Devam etme komutları

```bash
cd Technology-Knowledge-Base
python3 tools/autokb.py status
python3 tools/autokb.py backlog status
python3 -m unittest discover -s tools/tests
python3 tools/kb.py check
```
