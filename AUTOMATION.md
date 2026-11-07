# Otonom Araştırma Sistemi

Bu belge, bilgi tabanını her gün yeni bilimsel araştırmalarla besleyen, bunları taksonomiye yerleştiren,
yeni teknoloji adaylarını tespit eden ve `_index.md` dosyalarını kaynaklı bilgiyle güncel tutan sistemi anlatır.
Sistem bağımsızdır: web arayüzü, sunucu, veritabanı veya Docker yoktur. Kalıcı arşiv Markdown dosyalarıdır.

## Bileşenler

| Bileşen | Kod | Görev |
|---|---|---|
| Research Collector | `tools/kbresearch/sources/` | arXiv, OpenAlex (dergi/konferans + bioRxiv/medRxiv), Crossref |
| Research Classifier | `tools/kbresearch/classify.py` | Kayıtları kalıcı teknoloji `id`'lerine eşler (önce deterministik, gerekirse LLM) |
| Arşiv | `tools/kbresearch/archive.py` | Tek kanonik dosya, mükerrer tespiti, ön baskı ↔ yayın birleştirme, inceleme kuyruğu |
| Technology Discovery | `tools/kbresearch/discovery.py` | Taksonomide olmayan kavramları kanıtla aday yapar |
| Knowledge Maintainer | `tools/kbresearch/maintainer.py` | `_index.md` bölümlerini kaynaklı doldurur; güncellemeleri öneri olarak yazar |
| Akış | `tools/kbresearch/pipeline.py`, `tools/autokb.py` | Günlük çalışma, tarihsel tamamlama, kimlik ve geri çekme denetimi |
| Mevcut araç | `tools/kb.py` | İndeksleme, doğrulama, taksonomi işlemleri (korundu ve genişletildi) |

## Araştırma kaybı önleme (v2.1)

Önceki sürümde günlük 40 kayıt bütçesine sığmayan yüksek güvenli kayıtlar "görüldü" işaretlenip atılıyordu
(11-05 ve 11-06 çalışmalarında toplam 1.079 kayıt). Şimdi:

1. Yüksek güvenli her kayıt önce **kalıcı backlog'a** (`state/backlog.json`, kayıt başına ~200 bayt kimlik +
   sınıflandırma) girer. Çalışma sonunda backlog'dan öncelik sırasıyla en fazla `KB_MAX_ARCHIVE_PER_RUN` kayıt
   arşivlenir: önce hiç araştırması olmayan teknolojiler (+3), az araştırmalılar (+1), sonra puan, atıf ve hakemli
   yayın. Tam metadata arşivlenirken kaynaktan yeniden çekilir (arXiv `id_list`, OpenAlex `openalex_id` filtresi).
2. Backlog sınırları (toplam 3.000, teknoloji başına 30) aşılırsa en düşük öncelikliler **silinmez**,
   `state/ledger/YYYY-MM.jsonl.gz` defterine yazılır (`autokb.py backlog restore [--tech ID]` ile geri alınır).
3. İnceleme kuyruğu da aynı defteri kullanır: çalışma başı sınırı, toplam sınır ve süre aşımı → defter.
4. Eski sürümde atılan kayıtlar için ilk çalışmada **tek seferlik kurtarma**: `run-log`'dan bütçe nedeniyle kayıt
   atlanan günler bulunur ve yeniden taranır (arşivde olanlar atlanır, diğerleri backlog'a girer).

Bilinçli karar: bütçe artırılmadı. Yüksek güvenli akış günde ~550 kayıt; hepsini Markdown olarak arşivlemek depoyu
yılda ~600 MB büyütür. Bütçe kalite ve kapsama göre harcanır, kalan kayıtların kimliği kaybolmaz.

## Geç dizinlenen yayınlar (v2.1)

- OpenAlex'te `from_created_date` ücretli olduğundan aynı **yayın günü** ilk taramadan 10 ve 30 gün sonra yeniden
  taranır; yalnızca `created_date` ilk taramadan sonra olan kayıtlar işlenir (geri kalanlar zaten görülmüştü).
- arXiv gönderim günü 7 gün sonra yeniden taranır (geç duyurulanlar; görülen arXiv kimlikleri 21 gün hatırlanır).
- Anahtarla (`OPENALEX_API_KEY`) dergi akışı günün tamamını kapsar (≤100 sayfa); anahtarsız 20 sayfa.
- Tahmini OpenAlex maliyeti: ilk tarama ~95 + iki yeniden tarama ~190 liste çağrısı × $0,0001 ≈ **$0,03/gün**
  (ücretsiz anahtarın $1/gün bütçesinin %3'ü); keşif ve tarihsel tamamlama aramalarıyla toplam ≈ $0,05/gün.

## Sınıflandırma kalibrasyonu (v2.1)

`tools/kbresearch/eval/calibration-2026-10-29.jsonl`: 2026-10-29 arXiv + 2026-10-31 OpenAlex'ten puan aralıklarına
göre katmanlı 90 kayıt, elle değerlendirildi (doğru dal):

| Puan | 3–4,5 | 4,5–6 | 6–7,5 | 7,5–9 | 9+ |
|---|---|---|---|---|---|
| Kesinlik | 0,56 | 0,72 | 0,72 | 0,94 | 0,94 |

Yüksek güven eşiği 6,0 → **7,5** yapıldı (6–7,5 aralığı artık inceleme kuyruğuna gider). Bağımsız etiketli sette
(`classification-gold.jsonl`, 70 kayıt) arşive giren sınıfın kesinliği 0,94 → **1,00** (n=33 → 22). Düşük güvenli
kayıtlar hiçbir zaman arşive yazılmaz; yerel LLM'in sınıflandırma kararıyla da arşive yazılmaz (yalnızca öneri).

## Aday çakışma kontrolü (v2.1)

- Kısaltma eşleşmesi tek başına eş anlamlılık sayılmaz: adlar arasında sözcük örtüşmesi de gerekir
  (ör. "artificial neural network (ANN)" ≠ "approximate nearest neighbor search (ANN)" → *belirsiz kısaltma*).
- Jaccard ≥ 0,8 → `duplicate_of` ile ret; mevcut ad aday içinde geçiyorsa `variant_of` (alt tür);
  başka bir düğümle ≥ 0,4 örtüşme → `possible_duplicate` (onay için `--force` gerekir).
- Eski sürümün yalnızca kısaltmaya dayalı ret kararları yeniden değerlendirilip geri alınır.

## Günlük çalışma (`python3 tools/autokb.py daily`)

1. **arXiv**: gönderim tarihi `bugün-2` olan tüm kapsam içi kategorilerdeki ön baskılar (sayfa sayfa; 3 sn'de 1 istek).
2. **OpenAlex**: yayın tarihi `bugün-3` olan dergi/konferans makaleleri (Yaşam, Fizik, Sağlık bilimleri alanları,
   İngilizce, özetli) ve bioRxiv/medRxiv ön baskıları. Genel depolar (ör. Zenodo) kalite gerekçesiyle alınmaz.
   arXiv kayıtları OpenAlex'ten tekrar çekilmez.
3. Aynı çalışmanın kayıtları DOI/arXiv anahtarlarıyla birleştirilir; görülen kayıtlar 60 gün hatırlanır.
4. **Sınıflandırma**: `high` → backlog → öncelik sırasıyla arşiv, `medium` → inceleme kuyruğu, `low` → arşive alınmaz.
5. **Kimlik doğrulama**: DOI'ler Crossref'te (yoksa doi.org tanıtıcı API'sinde) doğrulanır; yayın türü ve
   ön baskı/yayın ilişkileri eklenir. Bulunamayan DOI inceleme kuyruğuna düşer.
6. **Geri çekme / düzeltme**: arşivdeki DOI'ler sırayla Crossref `updates:` filtresiyle denetlenir (Retraction Watch
   verisi dahil). Geri çekilen kayıtta uyarı bandı, indekslerde ⚠ işareti ve dayanan `_index.md` için öneri oluşur.
7. **Keşif**: metinde tanımlanan kısaltmalı teknik adlar ("Hypergraph Neural Networks (HGNNs)") izlenir; en az
   5 makale, 3 farklı ilk yazar ve 2 farklı ay (ya da 10 makale) eşiğini geçen ifade aday olur; literatür sayımı
   OpenAlex'ten alınır. Mevcut bir kısaltmayla çakışan ad eş anlamlı olarak reddedilir.
8. **Tarihsel tamamlama**: `state/backfill-queue.json` kuyruğundaki teknolojiler için adı başlıkta geçen, en çok atıf
   alan dergi/konferans yayınları; yalnızca sınıflandırıcı yüksek güvenle aynı dala yerleştirirse arşivlenir.
9. **Bilgi bakımı** (yalnızca LLM varsa): boş `_index.md` bölümleri öncelik sırasıyla (ana disiplin → alt disiplin →
   aile → yöntem) kaynaklı doldurulur; yeni araştırmalar içerikli düğümler için değerlendirilir ve yalnızca öneri yazılır.
10. `kb.py reindex`; iş akışında ardından `kb.py check` ve testler.

Her sayfadan sonra durum (`state/`) diske yazılır; çalışma kesilirse aynı gün/sayfadan devam eder. Bir kaynak
erişilemezse diğer adımlar sürer ve çıkış kodu `2` (kısmi) olur.

## Güvenlik ve inceleme

| İşlem | Otomatik mi? |
|---|---|
| Araştırma dosyası oluşturma / birleştirme | Evet (yalnızca `high` güven) |
| Orta güvenli sınıflandırma | Hayır → `review/CLASSIFICATION-QUEUE.md` (en fazla 150, öncelik sıralı; `autokb.py queue resolve N --tech ID`) |
| Yeni teknoloji klasörü | Hayır → `review/TECHNOLOGY-CANDIDATES.md` (`autokb.py candidates verify KEY --parent ID`) |
| Taşıma / yapısal değişiklik | Hiçbir zaman otomatik değil |
| Boş `_index.md` bölümünü kaynaklı doldurma | Evet (`content_status: ai_draft_sourced`, `content_verified: false`) |
| Dolu bölümü değiştirme, çelişki, geri çekme etkisi | Hayır → `review/index-proposals/` (`autokb.py proposals apply FILE`) |
| `content_verified: true` | Yalnızca insan |

GitHub Actions değişiklikleri **yalnızca `auto/research` dalına** gönderir ve `main` için pull request açar.

### Doğrulayıcı kuralları (bilgi bakımı)
Her ifade en az bir kaynak kimliğine bağlı olmalı; bilinmeyen kaynak, URL içeren ya da çok kısa/uzun ifadeler atılır.
Yalnızca ön baskıya dayanan ifade "(ön baskı bulgusu)" olarak işaretlenir; kaynaklar arası uyuşmazlık
"Sınırlılıklar" bölümünde ⚖ ile ayrıca gösterilir. LLM yalnızca özetleri görür; tam metin okunmuş gibi davranmaz.

### Lisans
Depo herkese açık olduğundan özetler yalnızca lisans izin veriyorsa kopyalanır (arXiv metadata CC0; OpenAlex
kaydında `cc0`/`cc-by`/`cc-by-sa`). Aksi hâlde araştırma dosyası özete bağlantı verir (`content_status: metadata_only`).

## Kaynaklar ve sınırlar (2026-11-05'te belgelerden ve canlı API'den doğrulandı)

| Kaynak | Erişim / kimlik | Hız sınırı | Sayfalama | Güncelleme | Kullanım |
|---|---|---|---|---|---|
| arXiv API | Anahtarsız; metadata CC0 | 3 sn'de 1 istek, tek bağlantı | `start`/`max_results` | `submittedDate` aralığı | Ön baskılar (kategori etiketi) |
| OpenAlex | Anahtarsız: IP başına paylaşılan $0,10/gün; ücretsiz anahtar: $1/gün | anahtarsız 10/sn | `page` (≤10.000 sonuç); imleç için anahtar | `from_publication_date` (`from_created_date` ücretli) | Dergi/konferans, bioRxiv/medRxiv, literatür sayımı, tarihsel tamamlama |
| Crossref | Public havuz (anahtarsız); `mailto` ile polite | public 5/aralık, eşzamanlılık 1 | `cursor` | `updates:` filtresi | DOI doğrulama, ilişkiler, düzeltme/geri çekme |
| doi.org Handle API | Anahtarsız | — | — | — | Crossref dışı DOI varlık kontrolü |
| bioRxiv/medRxiv API | Anahtarsız | belgelenmemiş | cursor | tarih aralığı | **Kullanılmıyor**: OpenAlex aynı kayıtları veriyor |
| Semantic Scholar | Anahtar önerilir (1 istek/sn) | paylaşımlı havuz | — | — | **Kullanılmıyor (v1)**: OpenAlex ile büyük ölçüde örtüşüyor |

Ölçülen gerçek maliyet: OpenAlex liste çağrısı $0,0001, arama $0,001 (`meta.cost_usd`). Tam günlük kapsam ve iki
yeniden tarama ile ≈ 285 liste + ≤20 arama ≈ **$0,05/gün** → ücretsiz anahtarın ($1/gün) %5'i. `OPENALEX_API_KEY`
tanımlı (2026-11-05).

## LLM ile bilgi doldurma (ücretsiz)

### Seçenek karşılaştırması (2026-11-07)

| Seçenek | Ücret / kota | Actions'ta kullanılabilirlik | Durum |
|---|---|---|---|
| **Yerel model, runner CPU'su** (llama.cpp + Qwen3-4B-Instruct-2507, Apache-2.0) | Ücretsiz; kota yok; anahtar/hesap yok | **Doğrulandı**: run 42302514951, 42311304315 | **Seçildi** |
| GitHub Models | — | — | 30 Temmuz 2026'da kapatıldı (GitHub belgeleri) |
| Gemini API ücretsiz katmanı (Flash) | Proje başına değişken; kaynaklar 20–1.500 istek/gün bildiriyor; Google yayımlanmış sabit sınır vermiyor | Anahtar gerekir (kullanıcı hesabı); doğrulanmadı | Kalite yükseltmesi için önerilen yol (`KB_LLM_PROVIDER=openai`) |
| Groq ücretsiz katmanı | ~1.000 istek, ~200 bin token/gün (gpt-oss, Qwen; üçüncü taraf kaynaklar) | Anahtar gerekir; doğrulanmadı | Alternatif |
| OpenRouter `:free` | 50 istek/gün ($10 altı bakiye) | Anahtar gerekir; ücretsiz modeller sık değişir | Uygun değil |
| Cloudflare Workers AI | 10.000 neuron/gün | Hesap gerekir; küçük modeller | Uygun değil |
| Claude API | Ücretli | Çalışır | Kullanıcı talimatıyla kullanılmıyor |

Kotalar hızla değişiyor; anahtar gerektiren seçenekler kullanıcı hesabı olmadan Actions'ta doğrulanamadı.

### Pilot sonuçları (10 düğüm, derinlik 1–8)

| | Qwen3-4B-Instruct-2507 | Qwen3.5-4B |
|---|---|---|
| Doğrulamadan geçen ifade (1. çalışma) | 90, 8 düğüm | 56, 6 düğüm |
| Dil | Türkçe | İngilizce (talimata uymadı) |
| Hız (runner CPU) | ~4,5–12 token/sn; düğüm başına 4–10 dk | ~12 token/sn |

Elle denetim (Claude, bu oturumda): ilk çalışmada Türkçe ifadelerin **~%45**'i, sıkılaştırılmış doğrulayıcıdan sonra
kalan 30 ifadenin **%43**'ü anlamca doğruydu. Hatalar: terim çevirisi ("resist" → "reaktif", "nonaqueous" →
"sıvı olmayan"), alıntıda olmayan genelleme, yanlış konu. **Kaynak cümleyi seçme** ise güvenilirdi: alıntı modunda
29 alıntının 22'si (%76) doğru bölümde ve doğru konudaydı; tamamı kaynak özetinde birebir geçiyor.

**Karar: yerel model alıntı modunda çalışır.** Bölümlere yalnızca kaynakta birebir geçen, teknolojinin adını içeren
alıntılar yazılır (`content_status: ai_quotes_sourced`); Türkçe özet yazılmaz ("Türkçe özet bekliyor"). Türkçe özet
için daha güçlü bir model (`KB_LLM_PROVIDER=openai` + Gemini/Groq anahtarı, `KB_LLM_TEXT_MODE=summary`) ya da insan
gerekir. Pilot sonucu: 10 düğümün **9'u** 22 denetlenmiş alıntıyla dolduruldu (`eval/pilot-audit-exclude.txt`:
çıkarılan 7 alıntı); 19 kaynak bağlantısı doi.org ile doğrulandı, kırık yok. Difüzyon modelleri düğümünde model iki
çalışmada da boş yanıt verdi.

### Doğrulayıcı (tüm sağlayıcılar)

Her ifade: bilinen bir kaynağa atıf; 6–45 sözcüklük **birebir İngilizce alıntı** (kaynak özetinde geçmeli); alıntı
teknolojinin adını/takma adını içermeli; ifadedeki her sayı alıntıda geçmeli; özet modunda metin Türkçe olmalı;
aynı alıntı/ifade tekrar edilmez. "Ön baskı" işareti modelden değil kaynağın yayın türünden gelir.

### Günlük çalışma ve maliyet

Günlük iş akışı modeli SHA-256 doğrulamasıyla indirir/önbelleğe alır, llama.cpp sunucusunu başlatır ve en fazla
`KB_MAINTAIN_NODES` (3) düğümü doldurur. İçerik üretilemeyen düğüm 30 gün atlanır. Model başlamazsa bakım atlanır,
toplama etkilenmez. Kapatmak: depo değişkeni `KB_LLM_PROVIDER=none`. Yerel modelin sınıflandırma kararıyla arşive
kayıt yazılmaz. **LLM maliyeti: $0** (açık depoda Actions dakikaları ücretsiz).

## Durum dosyaları (`state/`, Git'e işlenir)

`checkpoints.json` (kaynak başına kalınan gün/sayfa, ilk tarama tarihleri, yeniden taramalar, kurtarma),
`backlog.json`, `ledger/*.jsonl.gz`, `seen.json` (yalnızca arXiv, 21 gün), `counters.json` (günlük bütçe),
`run-log.jsonl` (son 400 çalışma), `discovery-terms.json`, `backfill-queue.json`, `llm-cache.jsonl`.
SQLite yerine JSON seçildi: GitHub Actions diski geçicidir, durum Git'le taşınmalıdır; metin dosyaları
okunabilir fark üretir ve birleştirilebilir.

## Sınıflandırma doğruluğu

`python3 tools/autokb.py eval tools/kbresearch/eval/classification-gold.jsonl`

70 kayıtlık etiketli set (2026-10-27 arXiv + 2026-10-28 OpenAlex; ayar verisinden farklı günler):
`high` (arşive giren) sınıfında **doğru dal 0,94, tam düğüm 0,91** (n=33); `medium` 0,75 (n=8); `low` 0,10 (n=29).
Ayrıca ilk gerçek günlük çalışmada arşive giren 38 kaydın elle denetiminde 34'ü doğru dalda (0,89).
Etiketler bu geliştirme oturumunda Claude tarafından verildi; insan doğrulaması önerilir. Örneklem küçüktür.

## Sık kullanılan komutlar

```bash
python3 tools/autokb.py daily --no-llm            # yerelde günlük çalışma
python3 tools/autokb.py status
python3 tools/autokb.py queue list
python3 tools/autokb.py queue resolve 3 --tech graph-neural-networks
python3 tools/autokb.py candidates list
python3 tools/autokb.py candidates verify "hypergraph neural network" --parent graph-neural-networks --title-tr "Hiperçizge Sinir Ağları"
python3 tools/autokb.py backfill zero-knowledge-proofs quantum-error-correction --per-tech 3
python3 tools/autokb.py maintain --limit 3        # LLM gerekir
python3 tools/autokb.py proposals list
python3 -m unittest discover -s tools/tests
```
