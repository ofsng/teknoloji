# İlerleme Durumu

Çalışma kesilirse buradan devam edin. Her oturum sonunda güncelleyin.

## Tamamlanan aşamalar (2026-11-05)

| Aşama | Durum | Not |
|---|---|---|
| 1. Taksonomi araştırması | Tamam | arXiv taksonomisi çevrimiçi okundu; ACM CCS üst dalları ve OECD FORD yapısı ikincil kaynaklarla doğrulandı. Ayrıntı: SOURCES.md |
| 2. Ayrıntılı hiyerarşi | Tamam (ilk sürüm) | 30 ana disiplin, 3492 düğüm; tanımlar `tools/seed/*.tax` |
| 3. Dosya sistemi | Tamam | `python3 tools/kb.py build` ile oluşturuldu; her düğümde `_index.md` + `Arastirmalar/.gitkeep` |
| 4. Bağlantılar | Tamam | 358 ilişki (`related` / `depends_on` / `applied_in`), tüm hedefler doğrulandı |
| 5. İndeksleme | Tamam | TECHNOLOGIES, RESEARCH-INDEX, RELATIONSHIPS, STATS otomatik |
| 6. Doğrulama | Tamam | `kb.py check`: 0 hata, 0 uyarı, 170 bilgi notu (tek çocuklu düğüm / yaprak alt disiplin) |
| Örnek araştırma kayıtları | 3 kayıt | Vaswani+ 2017 (arXiv:1706.03762), Groth 2016 (IACR ePrint 2016/260), Shor 1997 (DOI 10.1137/S0097539795293172). Kimlik bilgileri çevrimiçi doğrulandı; içerik bölümleri boş. |

## Açık işler

- [ ] `_index.md` tanım ve içerik bölümlerini kaynaklı olarak doldurmak (şu an tüm düğümlerde `content_verified: false`).
- [ ] ACM CCS 2012 alt düğümlerini resmi ağaçla satır satır karşılaştırmak (dl.acm.org/ccs bu oturumda HTTP 403 verdi).
- [ ] OECD FORD alt alan adlarını Frascati Manual 2015 metniyle karşılaştırmak.
- [ ] MeSH ağacı ile Tıp/Biyoloji, IEEE Taxonomy ile EEE/Haberleşme dallarını karşılaştırmak.
- [ ] Görece sığ kalan disiplinleri derinleştirmek: İBE, Görüntüleme, Ulaşım, İnşaat, Maden, Makine, Sensör (her biri 27–80 düğüm).
- [ ] `check --verbose` çıktısındaki 77 tek çocuklu düğümü gözden geçirmek (çoğu gerçek alt türdür; kardeşleri henüz eklenmedi).

## Devam etme komutları

```bash
cd Technology-Knowledge-Base
python3 tools/kb.py check --verbose
python3 tools/kb.py stats
```
