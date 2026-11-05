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

## Günlük çalışma (`python3 tools/autokb.py daily`)

1. **arXiv**: gönderim tarihi `bugün-2` olan tüm kapsam içi kategorilerdeki ön baskılar (sayfa sayfa; 3 sn'de 1 istek).
2. **OpenAlex**: yayın tarihi `bugün-3` olan dergi/konferans makaleleri (Yaşam, Fizik, Sağlık bilimleri alanları,
   İngilizce, özetli) ve bioRxiv/medRxiv ön baskıları. Genel depolar (ör. Zenodo) kalite gerekçesiyle alınmaz.
   arXiv kayıtları OpenAlex'ten tekrar çekilmez.
3. Aynı çalışmanın kayıtları DOI/arXiv anahtarlarıyla birleştirilir; görülen kayıtlar 60 gün hatırlanır.
4. **Sınıflandırma**: `high` → arşiv (bütçe dahilinde), `medium` → inceleme kuyruğu (LLM varsa önce LLM'e sorulur),
   `low` → arşive alınmaz.
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
| Orta güvenli sınıflandırma | Hayır → `review/CLASSIFICATION-QUEUE.md` (`autokb.py queue resolve N --tech ID`) |
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

Ölçülen gerçek maliyet: OpenAlex liste çağrısı $0,0001, arama $0,001 (`meta.cost_usd`). Günlük çalışma ≈ 25 liste +
≤10 arama ≈ **$0,01/gün** → ücretsiz anahtarın %1'i. GitHub runner'ları IP paylaştığından anahtarsız bütçeye
güvenilmemeli: `OPENALEX_API_KEY` tanımlayın.

## LLM modu (isteğe bağlı)

`ANTHROPIC_API_KEY` ve `pip install "anthropic>=1,<2"` ile açılır. Varsayılan model `claude-opus-5-5` ($4 / $20
milyon token); `KB_LLM_MODEL` ile değiştirilebilir — model değiştirmeden önce `tools/kbresearch/eval/` setiyle doğruluk
ölçülmeli. Yapılandırılmış çıktı (JSON şeması) ve sunucu tarafı ret geri dönüşü kullanılır; yanıtlar
`state/llm-cache.jsonl`'de önbelleklenir, aynı istem ikinci kez gönderilmez. Günlük sınırlar: `KB_LLM_MAX_CALLS`
(40), `KB_LLM_MAX_USD` ($1). Bütçe dolunca işlem durur, kalan iş sonraki çalışmaya kalır.

Tahmini maliyet (Opus 5.5, tahmindir; gerçek kullanım `state/counters.json`'a yazılır): sınıflandırma ≈ $0,01–0,02/kayıt,
bölüm doldurma ≈ $0,05–0,10/düğüm, güncelleme değerlendirmesi ≈ $0,02/kayıt → varsayılan sınırlarla **en fazla ≈ $1/gün**.

## Durum dosyaları (`state/`, Git'e işlenir)

`checkpoints.json` (kaynak başına kalınan gün/sayfa), `seen.json` (60 gün), `counters.json` (günlük bütçe),
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
