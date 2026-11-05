# Taksonomi İlkeleri ve Kararları

Bu belge sınıflandırmanın nasıl kurulduğunu, hangi kaynaklara dayandığını ve tartışmalı kanonik konum
kararlarının gerekçelerini açıklar. Tam ağaç için [TECHNOLOGIES.md](TECHNOLOGIES.md), kaynaklar için
[SOURCES.md](SOURCES.md), sayılar için [STATS.md](STATS.md).

## 1. Hiyerarşi modeli

`Ana disiplin → Alt disiplin → Teknoloji ailesi → Teknoloji → Alt teknoloji → Yöntem / uzmanlaşmış teknoloji`

Seviye sayısı sabit değildir: dallar 2 ile 8 seviye arasındadır (en derin örnek: `Bilgisayar-Bilimleri › … › Blokzincir › Olceklendirme › Katman-2 › Rollups › Optimistic-Rollups`). Dallar yalnızca
gerçek bir alt-tür, ayrı yöntem ailesi veya literatürde ayrı ele alınan teknik sınıf olduğunda açıldı.

**Alt klasör açma kriterleri** (en az biri):
1. Bağımsız ve tanınmış bir araştırma alanı (ör. arXiv kategorisi, ACM CCS düğümü, IEEE topluluğu, konferans serisi).
2. Kendine özgü algoritma veya yöntemler.
3. Literatürde ayrı bir teknik sınıf olarak ele alınması (derleme makaleleri, standartlar).
4. Kendine özgü donanım veya mimari yaklaşım.
5. Daha genel bir teknolojinin açıkça tanımlanmış alt türü.

Alt sınıflandırması anlamlı olmayan düğümler **yaprak** olarak bırakıldı.

## 2. Teknoloji ≠ şirket ≠ ürün ≠ sektör

- Şirketler (OpenAI), ticari ürünler (ChatGPT, Bitcoin), ürün aileleri ve kullanım sektörleri (FinTech, DeFi)
  klasör olarak **açılmadı**.
- Ürün ve standart adları yalnızca `aliases` alanında, teknolojiyi tanımaya yardımcı olacak örnek olarak geçer
  (ör. `Wi-Fi` klasörü, `IEEE-802.11` referansı; `Transformer` ailesinde `GPT`, `BERT` takma adları).
- Uygulama alanları `applied_in` ilişkisiyle gösterilir.
- Klinik tıp uzmanlıkları ve “Robot Türleri” gibi bazı gruplayıcı düğümler teknoloji değil bağlam sınıfıdır;
  bunlar `classification_confidence: medium` olarak işaretlendi.

## 3. Kanonik konum ve tekrar önleme

Her teknolojinin tek bir klasörü vardır. Birden fazla disiplini ilgilendiren konular aşağıdaki kararlarla
yerleştirildi; diğer disiplinlerle bağ `related` / `depends_on` / `applied_in` ilişkileriyle kurulur
([RELATIONSHIPS.md](RELATIONSHIPS.md)).

| Konu | Kanonik konum | Gerekçe |
|---|---|---|
| Yapay Zeka | Bilgisayar Bilimleri › Yapay Zeka | ACM CCS (Computing methodologies), arXiv cs.AI/cs.LG, OECD FORD 1.2. Görev listesinde ayrı madde olsa da ana disiplin yapılmadı; ayrı ana klasör “aynı disiplinin iki ana klasörde bulunması” kuralını ihlal ederdi. |
| Genetik ve Genomik | Biyoloji ve Biyoteknoloji › Genetik ve Genomik | OECD FORD 1.6 (Biological sciences) ve MeSH Genetics; aynı gerekçe. |
| Kriptografi | Bilgisayar Bilimleri › Kriptografi | arXiv cs.CR, ACM CCS Security and privacy › Cryptography. Matematik ile bağı sayılar teorisi düğümlerinden `applied_in` ile. |
| Blokzincir | Bilgisayar Bilimleri › Dağıtık ve Paralel Hesaplama › Dağıtık Defter Teknolojileri | Blokzincir bir DLT türüdür; konsensüs ve kriptografi bağımlılıkları `depends_on` ile. |
| Kuantum Makine Öğrenmesi | Kuantum Bilimleri › Kuantum Hesaplama › Kuantum Algoritmaları | Yöntemleri kuantum algoritmasıdır; ML ile `related`. |
| Kuantum Anahtar Dağıtımı | Kuantum Bilimleri › Kuantum İletişimi | Kriptografi altında ayrıca açılmadı. |
| Nöromorfik Hesaplama | Nörobilim ve Nöroteknoloji › Nöromorfik Mühendislik | Kaynağı nöral ilhamlı donanımdır; SNN ve memristörlerle `related`. |
| Biyoenformatik / Hesaplamalı Biyoloji | Biyoloji › Biyoenformatik ve Hesaplamalı Biyoloji | arXiv q-bio.QM, OECD 1.6. |
| Fotonik Hesaplama | Optik ve Fotonik › Fotonik Hesaplama | Donanım temeli fotoniktir. |
| Kontrol Teorisi, Optimal Kontrol | Mekatronik ve Kontrol Sistemleri › Kontrol Teorisi | arXiv eess.SY; matematikteki tekrar kaldırıldı. |
| Ağ protokolleri (TCP/IP, yönlendirme) | Bilgisayar Bilimleri › Bilgisayar Ağları | ACM CCS Networks, IETF. Fiziksel katman, kablosuz ve hücresel sistemler Haberleşme altında. |
| Bilgisayar Mimarisi | Bilgisayar Bilimleri | ACM CCS Computer systems organization, arXiv cs.AR. Entegre devre tasarımı ve yarı iletken üretimi Elektrik-Elektronik altında. |
| Bellek cihazları (DRAM, NAND, MRAM, ReRAM) | Veri Depolama ve Bellek Teknolojileri | Cihaz fiziği Fizik/Malzeme ile `related`/`depends_on`. Dosya sistemleri İşletim Sistemleri, dağıtık depolama Dağıtık Hesaplama altında. |
| Nanomalzemeler (grafen, CNT, 2B malzemeler) | Nanoteknoloji › Nanomalzemeler | OECD FORD 2.10; Malzeme Bilimi bağlar. |
| Görüntü sensörleri, ekranlar | Görüntüleme ve Görselleştirme | Tıbbi görüntüleme Tıp altında; bilgisayar grafikleri Bilgisayar Bilimleri altında; bilgi görselleştirme İBE altında. |
| Kuantum sensörler, atom saatleri | Kuantum Bilimleri › Kuantum Algılama ve Metroloji | Klasik metroloji Sensör ve Ölçüm altında, `related` ile. |
| Biyosensörler | Tıp ve Biyomedikal › Biyomedikal Mühendisliği | Nanosensörlerle `related`. |
| Nükleer fizik vs. nükleer teknoloji | Temel kuram Fizik altında; reaktör, yakıt çevrimi, füzyon mühendisliği Nükleer Teknolojiler altında | |
| Nükleer uzay itkisi | Uzay ve Havacılık › Uzay İtkisi | Fisyon reaktörlerine `depends_on`. |
| Astronomi ve Astrofizik | Fizik altında | arXiv astro-ph, OECD FORD 1.3. |
| İklim bilimi vs. iklim teknolojileri | Bilim Yer ve Gezegen Bilimleri altında; azaltım/uyum teknolojileri Çevre ve İklim altında | |
| Petrol mühendisliği | Maden, Mineral ve Petrol Mühendisliği | OECD FORD 2.7; Enerji’den `related`. |
| Biyomekanik | Makine Mühendisliği › Biyomekanik | Tıptaki tekrar kaldırıldı. |

## 4. Görev listesine eklenen ana disiplinler

- **Yer ve Gezegen Bilimleri** (OECD FORD 1.5): iklim bilimi, jeofizik, uzaktan algılama için kanonik konum gerekiyordu.
- **Maden, Mineral ve Petrol Mühendisliği** (OECD FORD 2.7): kaynak çıkarımı teknolojileri başka hiçbir disipline tam oturmuyordu.

## 5. Bilinçli olarak kapsam dışı bırakılanlar

Sosyal bilimler, beşeri bilimler, ekonomi ve finans (arXiv econ/q-fin; yalnızca Matematiksel Finans kalmıştır),
psikoloji (bilişsel nörobilim hariç), savunma teknolojileri (sektör; ilgili teknolojiler radar, itki vb. kendi
disiplinlerinde). İhtiyaç olursa `add-tech --parent root` ile yeni ana disiplin eklenebilir.

## 6. Güven ve durum işaretleri

- `status: emerging` — aktif araştırma, olgunlaşmamış teknoloji; `historical` — artık ana akım olmayan;
  `theoretical` — henüz pratik gerçeklemesi olmayan.
- `classification_confidence: medium/low` — kaynaklar arasında konum konusunda uzlaşı zayıf veya düğüm
  gruplayıcı nitelikte. Bu düğümler TECHNOLOGIES.md’de etiketle gösterilir.
- `content_verified: false` — tüm düğümlerde varsayılan; tanım ve teknik içerik henüz kaynakla doldurulmadı.
  (Ana disiplinlerin 1. bölümündeki kısa kapsam tanımları sınıflandırma kararlarını açıklar; kaynaklı tanım değildir.)

## 7. Ana disiplinler

<!-- AUTO:BEGIN (kb.py reindex üretir; bu bloğu elle düzenlemeyin) -->
| Ana disiplin | Klasör | Düğüm | Sınıflandırma referansları |
|---|---|---|---|
| [Bilgisayar Bilimleri](Bilgisayar-Bilimleri/_index.md) | `Bilgisayar-Bilimleri/` | 858 | OECD-FORD:1.2, ACM-CCS-2012, arXiv:cs |
| [Biyoloji ve Biyoteknoloji](Biyoloji-ve-Biyoteknoloji/_index.md) | `Biyoloji-ve-Biyoteknoloji/` | 147 | OECD-FORD:1.6, OECD-FORD:2.9, arXiv:q-bio, MeSH |
| [Çevre ve İklim Teknolojileri](Cevre-ve-Iklim-Teknolojileri/_index.md) | `Cevre-ve-Iklim-Teknolojileri/` | 63 | OECD-FORD:2.7, OECD-FORD:1.5, IPCC-AR6-WGIII, OECD-ENV-TECH |
| [Elektrik ve Elektronik Mühendisliği](Elektrik-ve-Elektronik-Muhendisligi/_index.md) | `Elektrik-ve-Elektronik-Muhendisligi/` | 210 | OECD-FORD:2.2, arXiv:eess, IEEE-Taxonomy |
| [Enerji Teknolojileri](Enerji-Teknolojileri/_index.md) | `Enerji-Teknolojileri/` | 121 | OECD-FORD:2.7, IEA-ETP, IPCC-AR6-WGIII |
| [Fizik ve Uygulamalı Fizik](Fizik-ve-Uygulamali-Fizik/_index.md) | `Fizik-ve-Uygulamali-Fizik/` | 163 | OECD-FORD:1.3, arXiv:physics, arXiv:cond-mat, arXiv:hep, arXiv:astro-ph, PACS |
| [Görüntüleme ve Görselleştirme Teknolojileri](Goruntuleme-ve-Gorsellestirme-Teknolojileri/_index.md) | `Goruntuleme-ve-Gorsellestirme-Teknolojileri/` | 50 | IEEE-SPS, SPIE, IS&T, SID |
| [Haberleşme ve Telekomünikasyon](Haberlesme-ve-Telekomunikasyon/_index.md) | `Haberlesme-ve-Telekomunikasyon/` | 111 | OECD-FORD:2.2, IEEE-ComSoc, ITU-T, 3GPP |
| [İnşaat ve Altyapı Teknolojileri](Insaat-ve-Altyapi-Teknolojileri/_index.md) | `Insaat-ve-Altyapi-Teknolojileri/` | 52 | OECD-FORD:2.1, ASCE |
| [İnsan-Bilgisayar Etkileşimi](Insan-Bilgisayar-Etkilesimi/_index.md) | `Insan-Bilgisayar-Etkilesimi/` | 45 | ACM-CCS:Human-centered-computing, arXiv:cs.HC, ISO-9241 |
| [Kimya ve Kimya Teknolojileri](Kimya-ve-Kimya-Teknolojileri/_index.md) | `Kimya-ve-Kimya-Teknolojileri/` | 112 | OECD-FORD:1.4, OECD-FORD:2.4, IUPAC |
| [Kuantum Bilimleri ve Teknolojileri](Kuantum-Bilimleri-ve-Teknolojileri/_index.md) | `Kuantum-Bilimleri-ve-Teknolojileri/` | 102 | arXiv:quant-ph, NIST-Quantum, ISO/IEC-JTC3 |
| [Maden, Mineral ve Petrol Mühendisliği](Maden-ve-Petrol-Muhendisligi/_index.md) | `Maden-ve-Petrol-Muhendisligi/` | 27 | OECD-FORD:2.7, SME, SPE |
| [Makine Mühendisliği](Makine-Muhendisligi/_index.md) | `Makine-Muhendisligi/` | 64 | OECD-FORD:2.3, ASME |
| [Malzeme Bilimi ve Mühendisliği](Malzeme-Bilimi/_index.md) | `Malzeme-Bilimi/` | 125 | OECD-FORD:2.5, arXiv:cond-mat.mtrl-sci |
| [Matematik ve Hesaplamalı Bilimler](Matematik-ve-Hesaplamali-Bilimler/_index.md) | `Matematik-ve-Hesaplamali-Bilimler/` | 212 | OECD-FORD:1.1, arXiv:math, arXiv:stat, MSC2020 |
| [Mekatronik ve Kontrol Sistemleri](Mekatronik-ve-Kontrol-Sistemleri/_index.md) | `Mekatronik-ve-Kontrol-Sistemleri/` | 51 | OECD-FORD:2.2, arXiv:eess.SY, IFAC, IEEE-CSS |
| [Nanoteknoloji](Nanoteknoloji/_index.md) | `Nanoteknoloji/` | 68 | OECD-FORD:2.10, ISO/TC-229, ISO/TS-80004 |
| [Nörobilim ve Nöroteknoloji](Norobilim-ve-Noroteknoloji/_index.md) | `Norobilim-ve-Noroteknoloji/` | 62 | MeSH:Neurosciences, arXiv:q-bio.NC, OECD-FORD:3.1 |
| [Nükleer Teknolojiler](Nukleer-Teknolojiler/_index.md) | `Nukleer-Teknolojiler/` | 66 | OECD-FORD:2.7, IAEA, arXiv:nucl-ex |
| [Optik ve Fotonik](Optik-ve-Fotonik/_index.md) | `Optik-ve-Fotonik/` | 77 | arXiv:physics.optics, Optica-OCIS, SPIE, OECD-FORD:1.3 |
| [Robotik ve Otonom Sistemler](Robotik-ve-Otonom-Sistemler/_index.md) | `Robotik-ve-Otonom-Sistemler/` | 76 | arXiv:cs.RO, IEEE-RAS, ISO-8373 |
| [Sensör ve Ölçüm Teknolojileri](Sensor-ve-Olcum-Teknolojileri/_index.md) | `Sensor-ve-Olcum-Teknolojileri/` | 61 | OECD-FORD:2.2, BIPM-SI, JCGM-VIM, IEEE-IMS |
| [Tarım ve Gıda Teknolojileri](Tarim-ve-Gida-Teknolojileri/_index.md) | `Tarim-ve-Gida-Teknolojileri/` | 78 | OECD-FORD:4.1-4.5, OECD-FORD:2.11, FAO-AGROVOC |
| [Tıp ve Biyomedikal Teknolojiler](Tip-ve-Biyomedikal-Teknolojiler/_index.md) | `Tip-ve-Biyomedikal-Teknolojiler/` | 152 | OECD-FORD:3.1-3.5, OECD-FORD:2.6, MeSH, IEEE-EMBS |
| [Ulaşım ve Mobilite Teknolojileri](Ulasim-ve-Mobilite-Teknolojileri/_index.md) | `Ulasim-ve-Mobilite-Teknolojileri/` | 55 | OECD-FORD:2.1, OECD-FORD:2.3, TRB-TRT, SAE |
| [Üretim ve Endüstri Teknolojileri](Uretim-ve-Endustri-Teknolojileri/_index.md) | `Uretim-ve-Endustri-Teknolojileri/` | 80 | OECD-FORD:2.3, CIRP, ISO/TC-261 |
| [Uzay ve Havacılık Teknolojileri](Uzay-ve-Havacilik-Teknolojileri/_index.md) | `Uzay-ve-Havacilik-Teknolojileri/` | 92 | OECD-FORD:2.3, AIAA, NASA-Technology-Taxonomy-2020 |
| [Veri Depolama ve Bellek Teknolojileri](Veri-Depolama-ve-Bellek-Teknolojileri/_index.md) | `Veri-Depolama-ve-Bellek-Teknolojileri/` | 47 | IRDS-Mass-Data-Storage, IEEE-Magnetics, SNIA |
| [Yer ve Gezegen Bilimleri](Yer-ve-Gezegen-Bilimleri/_index.md) | `Yer-ve-Gezegen-Bilimleri/` | 65 | OECD-FORD:1.5, arXiv:physics.geo-ph, arXiv:physics.ao-ph |
<!-- AUTO:END -->
