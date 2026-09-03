`n_clusters` bir girdi. Peki kaç yazacaksın? İki araç var ve bu
alıştırmada ikisini de kuracaksın.

**Yapman gerekenler:**

1. Veriyi hazırla ve ölçekle.
2. `k` değerini **2'den 8'e** kadar (8 dahil) dene. Her biri için tek satır
   yazdır: **k, eylemsizlik (bir ondalık), silüet (üç ondalık)**.
3. İki eğriyi **yan yana** çiz: solda eylemsizlik, sağda silüet. Eksenleri
   `k` ve sırasıyla `inertia` / `silhouette` diye adlandır, başlık koy ve
   `chart.png` olarak kaydet.
4. Son satırda **en yüksek silüeti veren `k`'yı** ve o silüeti yan yana
   yazdır.

**Beklenen çıktı:**

```
2 695.9 0.514
3 388.8 0.525
4 265.6 0.517
5 212.7 0.489
6 189.6 0.457
7 167.3 0.442
8 155.4 0.415
3 0.525
```

**Eylemsizlik sütunu her zaman düşüyor.** `k` kayıt sayısına eşit olsaydı
sıfır olurdu — yani "en düşük eylemsizlik" diye bir hedef yok. Bakılan şey
**nerede yavaşladığı**: 695.9 → 388.8 → 265.6 büyük düşüşler, sonra
212.7 → 189.6 → 167.3 yavaşlıyor. Buna **dirsek yöntemi** deniyor ve
buradaki dirsek 3 ile 4 arasında.

**Silüet `k=3` diyor.** Ama bu veri **dört gruptan** üretildi.

Silüet yanılmıyor; kendi sorusuna doğru cevap veriyor. Onun sorusu
"kümeler ne kadar derli toplu", "kaç gerçek grup var" değil. Birinci
alıştırmadaki küme 1 (nadir uğrayanlar) ile küme 2 (sık gelen browser'lar)
uzayda birbirine yakın duruyor; üçe indirince ikisi birleşiyor, silüet
0.008 artıyor ve **iş açısından anlamlı bir ayrım kayboluyor.**

0.525 ile 0.517 arasındaki fark zaten ölçüm gürültüsü kadar.

**Alınacak sonuç: `k` bir ölçüm sonucu değil, bir karar.** İki araç aralığı
daraltıyor — 2 ile 8 arası değil, 3 ile 4 arası. Gerisini profil
tablosuna bakan insan seçiyor.
