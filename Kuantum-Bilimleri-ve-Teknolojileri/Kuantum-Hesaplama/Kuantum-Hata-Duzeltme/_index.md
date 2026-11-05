---
id: quantum-error-correction
title: "Quantum Error Correction"
title_tr: "Kuantum Hata Düzeltme"
type: technology
parent: quantum-computing
status: established
classification_confidence: high
aliases: ["QEC"]
related: []
depends_on: ["coding-theory"]
applied_in: []
classification_refs: []
content_verified: false
created: 2026-11-05
layout: 2
content_status: ai_draft_sourced
content_sources: ["10.1146/annurev-conmatphys-031119-050605", "10.1088/1361-6633/ad1f81", "10.1146/annurev-conmatphys-031218-013618", "10.1093/nsr/nwaf246", "10.1103/physreva.54.3824", "10.1126/science.1231930", "10.1109/18.681315"]
last_maintained: 2026-11-05
---

# Kuantum Hata Düzeltme (Quantum Error Correction)

<!-- AUTO:NAV:BEGIN (otomatik; elle düzenlemeyin) -->
**Konum:** [Kök](../../../TECHNOLOGIES.md) › [Kuantum Bilimleri ve Teknolojileri](../../_index.md) › [Kuantum Hesaplama](../_index.md) › **Kuantum Hata Düzeltme**
<!-- AUTO:NAV:END -->

## 1. Tanım

- Kuantum hata düzeltme kodları (QECC), dolanıklık arıtma protokolleriyle birlikte kuantum durumlarını çevreyle etkileşimin yol açtığı bozulmalardan korumanın iki yolundan biridir; bir QECC ile keyfi bir kuantum durumu gürültülü bir kanal üzerinden belirli bir hızla bozulmadan iletilebilir. [1]

## 2. Çalışma prensibi

- Tek yönlü klasik iletişim kullanan bir dolanıklık arıtma protokolü, aynı kanal üzerinde aynı hızda bir kuantum hata düzeltme kodu verir ve bunun tersi de geçerlidir; kuantum hata düzeltme kodları ise arıtma protokollerinden farklı olarak klasik iletişim gerektirmez. [1]

## 3. Tarihçe

- 1996 tarihli bir çalışma, dolanıklık arıtma protokolleri ile kuantum hata düzeltme kodları arasındaki hız denkliğini kanıtlamıştır. [1]
- 1998 tarihli bir çalışma, kuantum hata düzeltme kodu bulma problemini GF(4) cismi üzerindeki toplamsal kodlara indirgemiş ve 30 kübite kadar uzunluktaki kodlar için alt ve üst sınır tabloları sunmuştur. [2]
- Süperiletken kuantum hesaplamada son yıllardaki deneysel ilerlemeler arasında yüzey kodlarına dayalı kuantum hata düzeltme gösterimleri yer almaktadır. [3]

## 4. Temel kavramlar

- Gürültülü orta ölçekli kuantum (NISQ) dönemi, hata düzeltmesi yapılmayan kübitlerle kuantum benzetimlerinin ve algoritmalarının çalıştırıldığı dönem olarak tanımlanır; hata düzeltmeli kuantum bilgisayarlar daha uzun vadeli bir hedeftir. [4]
- Mantıksal kübitler üzerindeki işlemler, genişletilebilir süperiletken kübit sistemlerinde gösterilmiştir. [4]
- Topolojik kuantum hata düzeltme, Majorana sıfır modlarına dayanan topolojik kübit tasarımlarıyla birlikte incelenmektedir. [5]

## 5. Temel yöntemler

- Kuantum hata düzeltme kodları, belirli bir iz iç çarpımına göre öz-ortogonal olan GF(4) üzerindeki toplamsal kodlar aracılığıyla oluşturulabilir. [2]
- Yüzey kodları (surface codes), süperiletken kuantum işlemcilerde deneysel olarak uygulanan hata düzeltme yöntemleri arasındadır. [3]
- Molekül nanomıknatıslarında çok seviyeli qudit'ler kullanılarak tek bir molekül içine gömülü hata düzeltmeli kübit kodlaması önerilmiştir; bu yaklaşımın standart çok kübitli kodlardaki büyük fiziksel kübit yükünü aşabileceği öne sürülmektedir. [6]

<!-- AUTO:BEGIN (kb.py reindex üretir; bu bloğu elle düzenlemeyin) -->
## 6. Alt teknolojiler

- [Bozonik Kodlar](Bozonik-Kodlar/_index.md)
- [Hata Toleranslı Kuantum Hesaplama](Hata-Toleransli-Kuantum-Hesaplama/_index.md)
- [Kuantum Hata Düzeltme Kod Çözücüleri](QEC-Kod-Cozuculeri/_index.md)
- [Stabilizatör Kodları](Stabilizator-Kodlari/_index.md)

## 7. İlişkili teknolojiler

- **Üst teknoloji:** [Kuantum Hesaplama](../_index.md)
- **Bağımlı olduğu (Depends on):** [Kodlama Teorisi](../../../Matematik-ve-Hesaplamali-Bilimler/Ayrik-Matematik/Kodlama-Teorisi/_index.md)
<!-- AUTO:END -->

## 8. Kullanım alanları

- Büyük ölçekli, hata düzeltmeli kuantum bilgisayarlar inşa etmek süperiletken kübit yaklaşımının uzun vadeli hedefi olarak tanımlanmaktadır. [4]
- Kuantum hata düzeltme kodları, kuantum durumlarının gürültülü kanallar üzerinden bozulmadan iletilmesinde kullanılır. [1]

## 9. Avantajlar

- Kuantum hata düzeltmenin amacı, doğası gereği dissipatif olan karmaşık aktif sistemlerin süresiz biçimde eşevreli kalacak şekilde tasarlanıp işletilmesidir. [7]

## 10. Sınırlılıklar

- Standart çok kübitli hata düzeltme kodları çok sayıda fiziksel kübit gerektirir (büyük ek yük). [6]
- %50 depolarize eden kanal gibi bazı gürültülü kanallar, iki yönlü klasik iletişim varsa kuantum durumlarının güvenilir iletiminde kullanılabilir; yalnızca tek yönlü iletişimle kullanılamaz. [1]

## 11. Açık problemler

- Çok sayıda kübitli, hata düzeltmeli bir bilgi işlemci inşa etmek, başlı başına yeni bir araştırma alanı oluşturan özgül mimari problemlerin çözülmesini gerektirmektedir. [7]
- Ölçeklendirme, süperiletken kuantum hesaplamada sürmekte olan temel zorluklar arasında gösterilmektedir. [3]

## 12. Önemli araştırmalar

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

<!-- AUTO:RESEARCH:BEGIN (otomatik; elle düzenlemeyin) -->
Arşivdeki kayıtlar — bu düğüm: **5**, alt teknolojiler dahil: **5**.

- [Mixed-state entanglement and quantum error correction](Arastirmalar/1996-Bennett-Mixed-state-entanglement-and.md) — Bennett vd. (1996) · *Physical Review A* · hakemli · atıf: 5158
- [Multiple-particle interference and quantum error correction](Arastirmalar/1996-Steane-Multiple-particle-interference-and.md) — Steane (1996) · *Proceedings of the Royal Society A Mathematical Physical and Engineering Sciences* · hakemli · atıf: 1579
- [Quantum error correction for quantum memories](Arastirmalar/2015-Terhal-Quantum-error-correction-for.md) — Terhal (2015) · *Reviews of Modern Physics* · hakemli · atıf: 1326
- [QECert: Formal Foundations for Quantum Error-Correction Theory in Lean](Arastirmalar/2026-He-QECert-Formal-Foundations-for.md) — He vd. (2026) · *arXiv* · ön baskı / hakemsiz
- [Trinetra.Q: Statistical and Behavioral Detection of Attacks on the Quantum-Error-Correction Layer and Classical Control Stack of Quantum Computing Systems](Arastirmalar/2026-Sipani-Trinetra-Statistical-and-Behavioral.md) — Sipani (2026) · *arXiv* · ön baskı / hakemsiz
<!-- AUTO:RESEARCH:END -->

## 13. Güncel gelişmeler

_Henüz doldurulmadı. Yalnızca doğrulanabilir kaynaklara dayanan bilgi ekleyin._

<!-- AUTO:RECENT:BEGIN (otomatik; elle düzenlemeyin) -->
Son 365 gündeki kayıtlar (alt teknolojiler dahil; yeni bulgular kesin sonuç değildir):

- [QECert: Formal Foundations for Quantum Error-Correction Theory in Lean](Arastirmalar/2026-He-QECert-Formal-Foundations-for.md) — He vd. (2026) · *arXiv* · ön baskı / hakemsiz
- [Trinetra.Q: Statistical and Behavioral Detection of Attacks on the Quantum-Error-Correction Layer and Classical Control Stack of Quantum Computing Systems](Arastirmalar/2026-Sipani-Trinetra-Statistical-and-Behavioral.md) — Sipani (2026) · *arXiv* · ön baskı / hakemsiz
<!-- AUTO:RECENT:END -->

## 14. Kaynaklar

1. Charles H. Bennett vd. (1996). *Mixed-state entanglement and quantum error correction*. Physical Review A. https://doi.org/10.1103/physreva.54.3824 — hakemli
2. A.R. Calderbank vd. (1998). *Quantum error correction via codes over GF(4)*. IEEE Transactions on Information Theory. https://doi.org/10.1109/18.681315 — hakemli
3. Yao-Yao Jiang vd. (2025). *Advancements in superconducting quantum computing*. National Science Review. https://doi.org/10.1093/nsr/nwaf246 — hakemli
4. Morten Kjærgaard vd. (2019). *Superconducting Qubits: Current State of Play*. Annual Review of Condensed Matter Physics. https://doi.org/10.1146/annurev-conmatphys-031119-050605 — hakemli
5. Yuval Oreg vd. (2019). *Majorana Zero Modes in Networks of Cooper-Pair Boxes: Topologically Ordered States and Topological Quantum Computation*. Annual Review of Condensed Matter Physics. https://doi.org/10.1146/annurev-conmatphys-031218-013618 — hakemli
6. Alessandro Chiesa vd. (2024). *Molecular nanomagnets: a viable path toward quantum information processing?*. Reports on Progress in Physics. https://doi.org/10.1088/1361-6633/ad1f81 — hakemli
7. Michel Devoret vd. (2013). *Superconducting Circuits for Quantum Information: An Outlook*. Science. https://doi.org/10.1126/science.1231930 — hakemli

