# Technology Knowledge Base

Bilim ve teknoloji alanlarını en genel disiplinlerden en özel teknik yöntemlere kadar sınıflandıran,
araştırmaların ilgili teknoloji klasöründe Markdown dosyaları olarak saklandığı kişisel bilgi arşivi.

- Yalnızca klasörler ve Markdown dosyalarından oluşur; internet, sunucu, veritabanı gerektirmez.
- Git ile sürümlenebilir; Obsidian, VS Code veya herhangi bir Markdown okuyucuyla gezilebilir.
- Bakım araçları yalnızca Python 3 standart kütüphanesini kullanır (`tools/kb.py`).

## Yapı

```
Technology-Knowledge-Base/
├── README.md            # bu dosya
├── TAXONOMY.md          # sınıflandırma ilkeleri, kanonik konum kararları (elle yazılır)
├── TECHNOLOGIES.md      # tüm teknolojilerin hiyerarşik indeksi (otomatik)
├── RESEARCH-INDEX.md    # tüm araştırma kayıtları (otomatik)
├── RELATIONSHIPS.md     # disiplinler arası ilişkiler (otomatik)
├── STATS.md             # sayım ve derinlik raporu (otomatik)
├── SOURCES.md           # sınıflandırmada kullanılan akademik kaynaklar (elle yazılır)
├── PROGRESS.md          # çalışma günlüğü / kaldığı yerden devam notları
├── templates/           # _index.md ve araştırma dosyası şablonları
├── tools/
│   ├── kb.py            # bakım aracı
│   └── seed/*.tax       # ilk kurulumda kullanılan taksonomi tanımları
└── <Ana-Disiplin>/
    └── <Alt-Disiplin>/
        └── <Teknoloji>/
            ├── _index.md        # teknoloji tanıtım dosyası (ön bilgi + bölümler)
            ├── Arastirmalar/    # yalnızca bu teknolojiye doğrudan ait çalışmalar
            │   └── 2016-Groth16.md
            └── <Alt-Teknoloji>/ ...
```

Her teknoloji klasöründe bir `_index.md` vardır. Klasör adları ASCII uyumlu Türkçedir
(`Sifir-Bilgi-Ispatlari`); dosya içerikleri doğru Türkçe karakterleri ve İngilizce teknik adları kullanır.

## `_index.md` biçimi

```yaml
---
id: zero-knowledge-proofs          # kalıcı, benzersiz kimlik (İngilizce addan türetilir)
title: "Zero-Knowledge Proofs"
title_tr: "Sıfır Bilgi İspatları"
type: technology                   # discipline | subdiscipline | technology
parent: cryptography               # üst teknolojinin id'si (ana disiplinlerde: root)
status: established                # established | emerging | historical | theoretical
classification_confidence: high    # high | medium | low
aliases: ["ZKP"]
related: []                        # İlişkili (Related)
depends_on: ["interactive-proof-systems"]
applied_in: []
classification_refs: []            # ör. arXiv:cs.CR, ACM-CCS:..., OECD-FORD:1.2
content_verified: false            # 1-2 ve 6-10 numaralı bölümler kaynakla doldurulunca true yapın
created: 2026-11-05
---
```

Gövdedeki **3. Üst teknoloji, 4. Alt teknolojiler, 5. İlişkili teknolojiler** bölümleri ve araştırma listesi
`<!-- AUTO:BEGIN -->` / `<!-- AUTO:END -->` arasında otomatik üretilir. Diğer bölümler (tanım, çalışma prensibi,
kavramlar, tarihçe, araştırma konuları, açık problemler, kaynaklar) elle ve **yalnızca doğrulanabilir kaynaklarla** doldurulur.
Araç bu bölümlerin üzerine asla yazmaz.

## Günlük kullanım

Tüm komutlar `Technology-Knowledge-Base/` içinden çalıştırılır.

```bash
python3 tools/kb.py suggest "spiking neural network"     # bir teknoloji nerede / nereye eklenmeli?
python3 tools/kb.py find zero-knowledge-proofs            # id -> klasör yolu
python3 tools/kb.py add-tech --parent zk-snarks --title "Lookup Arguments" --title-tr "Arama Argümanları" --status emerging --refs "IACR"
python3 tools/kb.py add-research --tech pairing-based-snarks --title "On the Size of Pairing-based Non-interactive Arguments" \
    --authors "Jens Groth" --year 2016 --url https://eprint.iacr.org/2016/260 --publication "EUROCRYPT 2016" \
    --type original --related zk-rollups --keywords "zk-SNARK,pairings" --short Groth16
python3 tools/kb.py reindex   # elle düzenlemeden sonra indeksleri ve AUTO bloklarını yenile
python3 tools/kb.py check     # doğrulama (hata varsa çıkış kodu 1)
python3 tools/kb.py stats
```

### Yeni araştırma ekleme kuralları

1. Araştırmanın **temel katkısını** belirleyin ve **en spesifik** teknoloji klasörünü seçin (`suggest` yardımcı olur).
2. Kaydı yalnızca o klasörün `Arastirmalar/` dizinine ekleyin; diğer teknolojileri `related_technologies` alanıyla bağlayın.
3. Kimlik (`research_id`) otomatik hesaplanır: `doi:<doi>` → yoksa `arxiv:<id>` (sürüm eki atılır) →
   yoksa `kb:<yıl>-<ilk-yazar-soyadı>-<başlık+yıl+yazar özetinin 8 hanesi>`. Aynı kimlik, aynı DOI/arXiv
   ya da aynı başlık+yıl ikinci kez eklenemez; `check` mevcut kayıtlar arasında da arar.
4. Bölümleri yalnızca makalenin kendisinden veya güvenilir ikincil kaynaklardan doldurun; emin olunmayan bilgi eklemeyin.
5. Ardından `python3 tools/kb.py check`.

### Yeni teknoloji ekleme kuralları

- Önce `suggest` ile aynı kavramın başka adla var olmadığını doğrulayın (araç aynı adlı teknolojiyi reddeder).
- Yeni klasör, `TAXONOMY.md` içindeki derinlik kriterlerinden en az birini karşılamalıdır.
- Şirket, ürün, sektör veya uygulama alanı adlarıyla klasör açmayın; bunları ilgili teknolojinin `applied_in`
  alanına veya metne yazın.
- Elle klasör eklerseniz `_index.md` ön bilgisindeki `parent` alanını üst klasörün `id`'siyle eşleştirip `reindex` + `check` çalıştırın.
- Bir teknolojiyi taşırken klasörü taşıyın, `parent` alanını güncelleyin, `reindex` çalıştırın; `id` değişmez,
  böylece ilişkiler ve araştırma kayıtları bozulmaz.

## Kaynak gerçeklik

Kurulumdan sonra **klasör ağacı ve `_index.md` ön bilgileri** esastır. `tools/seed/*.tax` yalnızca ilk kurulumun
belgesidir; `build` yeniden çalıştırılırsa yalnızca eksik klasörleri ekler, var olan hiçbir dosyanın üzerine yazmaz.
