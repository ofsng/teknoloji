# Sınıflandırma Kaynakları

Bu taksonomi aşağıdaki sınıflandırma sistemleri ve standartlar birleştirilerek kuruldu. Her `_index.md`
dosyasındaki `classification_refs` alanı ilgili düğümün dayandığı kodları gösterir (ör. `arXiv:cs.CR`,
`OECD-FORD:2.10`). Kodlar düğüm düzeyinde **yerleşim gerekçesi**dir; içerik doğrulaması değildir.

## Doğrulama durumu (2026-11-05)

| Kaynak | Bu çalışmada nasıl kullanıldı | Doğrulama |
|---|---|---|
| arXiv Category Taxonomy — <https://arxiv.org/category_taxonomy> | Bilgisayar bilimi, matematik, fizik, q-bio, eess, stat kategori kodları | Çevrimiçi okundu; tüm kategori kodları sayfadan alındı. |
| ACM Computing Classification System 2012 — <https://www.acm.org/publications/class-2012> | Bilgisayar bilimleri üst dalları (14 üst dal: Hardware, Computer systems organization, Networks, Software and its engineering, Theory of computation, Mathematics of computing, Information systems, Security and privacy, Human-centered computing, Computing methodologies, Applied computing …) | Üst dal listesi ikincil kaynaklarla doğrulandı; `dl.acm.org/ccs` ağaç sayfası erişimi engelledi (HTTP 403), alt düğümler doğrudan karşılaştırılamadı. |
| OECD Frascati Manual 2015, Fields of Research and Development (FORD) — <https://oe.cd/frascati> | Ana disiplin sınırları (1.x doğa bilimleri, 2.x mühendislik, 3.x tıp, 4.x tarım) | İki seviyeli yapı (6 ana alan, 42 alt alan) UN Statistics Division kaydıyla doğrulandı (<https://unstats.un.org/unsd/classifications/Family/Detail/1039>); alt alan adları model bilgisinden kullanıldı, belgeyle satır satır karşılaştırılmadı. |
| UNESCO UIS FORD sayfası — <https://uis.unesco.org/node/3079686> | FORD’un uluslararası kullanımı | Arama sonucu olarak görüldü. |
| MeSH (Medical Subject Headings), NLM | Tıp, genetik, nörobilim başlıkları | Çevrimiçi karşılaştırılmadı; terimler genel bilgiye dayanır. |
| IEEE Taxonomy / IEEE topluluk kapsamları (SPS, PES, PELS, RAS, ComSoc, EMBS, CSS) | Elektrik-elektronik, haberleşme, robotik alt dalları | Çevrimiçi karşılaştırılmadı. |
| NIST yayınları: SP 800-145 (bulut tanımı), SP 800-207 (Zero Trust), NIST PQC standardizasyonu, CSF | Bulut, sıfır güven, kuantum sonrası kriptografi düğümleri | Çevrimiçi karşılaştırılmadı. |
| ISO/IEC standartları: ISO/TS 80004 (nanoteknoloji terimleri), ISO/ASTM 52900 (eklemeli imalat yedi süreç kategorisi), ISO 8373 (robotik), ISO 26262, ISO/SAE 21434, ISO 21448, ISO 9241, ISO 14040, ISO 19650, ISO 13485, IEC 60601, IEC 61131/61499/62443, ISO 14721 (OAIS) | İlgili düğümlerin tanım ve alt bölümleri | Standart numaraları bilgi tabanından; metinler çevrimiçi okunmadı. |
| 3GPP / ITU-R IMT, IETF RFC’ler, IEEE 802 | Hücresel, kablosuz, ağ protokolü düğümleri | Çevrimiçi karşılaştırılmadı. |
| Generation IV International Forum (GIF) | Altı IV. nesil reaktör tipi | Çevrimiçi karşılaştırılmadı. |
| SAE J3016 | Otonom sürüş seviyeleri | Çevrimiçi karşılaştırılmadı. |
| NASA Technology Taxonomy 2020 | Uzay teknolojileri alt dalları | Çevrimiçi karşılaştırılmadı. |
| IPCC AR6 WG III | Karbon giderimi ve azaltım teknolojileri | Çevrimiçi karşılaştırılmadı. |
| BIPM SI Brochure, JCGM GUM/VIM | Metroloji düğümleri | Çevrimiçi karşılaştırılmadı. |
| Mathematics Subject Classification 2020 (MSC2020) | Matematik alt dalları | Çevrimiçi karşılaştırılmadı. |
| IRDS (International Roadmap for Devices and Systems) | Yarı iletken cihaz ve bellek dalları | Çevrimiçi karşılaştırılmadı. |

## Açık uyarılar

- Kaynaklar arasında uyuşmazlık olan konumlar için verilen kararlar [TAXONOMY.md](TAXONOMY.md) §3’tedir.
- “Çevrimiçi karşılaştırılmadı” işaretli kaynaklar için düğümler yerleşik akademik bilgiye dayanır; kesin bilimsel
  sınıflandırma olarak değil, gerekçeli bir öneri olarak okunmalıdır. `classification_confidence` alanı bu
  belirsizliği düğüm bazında gösterir.
- Hiçbir `_index.md` dosyasına kaynak gösterilmemiş teknik içerik eklenmedi; tanım bölümleri boş bırakıldı.
