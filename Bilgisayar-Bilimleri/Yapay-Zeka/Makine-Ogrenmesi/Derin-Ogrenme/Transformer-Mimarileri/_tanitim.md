---
node: transformer-architectures
intro_status: ai_draft_sourced
intro_version: 1
written: 2026-11-23
written_by: "Claude (yapay zekâ taslağı; kaynaklar Crossref/arXiv ile doğrulandı)"
human_verified: false
---

## Öz

Dikkat mekanizmasıyla bir dizideki bütün öğeleri birbirine aynı anda bağlayan ve bugün dil ile görüntü modellerinde yaygın kullanılan sinir ağı ailesi. [1, 2]

## Neden önemli

Tekrarlayan katmanları kaldırıp yalnızca dikkate dayanarak eğitimi paralel hâle getirdi ve makine çevirisinde dönemin en iyi sonuçlarını daha kısa eğitimle aştı. [1] Aynı yapı sonradan dilin yanı sıra görüntü gibi başka veri türlerine de uygulandı. [2, 4]

## Neler yapıldı

- **2017** · Yalnızca dikkat katmanlarından oluşan Transformer, makine çevirisi için tanıtıldı. [1]
- **2018** · BERT, etiketsiz metinle ön eğitip görevlere ince ayar yapma yaklaşımını yaygınlaştırdı. [3]
- **2020** · Görü Transformer'ı (ViT), görüntüyü yamalara bölerek sınıflandırmada evrişimli ağlarla yarıştı. [4]

## Bugün nerede

- Dil modelleme ve metin anlama [2, 3]
- Makine çevirisi [1]
- Görüntü tanıma [4]

## Neler bekleniyor

- Öz-dikkatin dizi uzunluğuyla karesel büyüyen hesaplama ve bellek maliyetini düşüren verimli yöntemler. [2]
- Bu verimli yöntemlerin farklı görevlerde tutarlı biçimde karşılaştırılması. [2]

## Kaynaklar

1. Vaswani, A. vd. (2017). Attention Is All You Need. NeurIPS 2017. https://arxiv.org/abs/1706.03762
2. Tay, Y. vd. (2022). Efficient Transformers: A Survey. ACM Computing Surveys. https://doi.org/10.1145/3530811
3. Devlin, J. vd. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. https://arxiv.org/abs/1810.04805
4. Dosovitskiy, A. vd. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. https://arxiv.org/abs/2010.11929
