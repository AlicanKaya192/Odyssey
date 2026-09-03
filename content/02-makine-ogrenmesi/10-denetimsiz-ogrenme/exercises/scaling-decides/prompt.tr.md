Bölüm 06'da KNN için ölçeklemenin zorunlu olduğunu ölçmüştün. Bölüm
07'de ağaç için gereksiz olduğunu. K-ortalamalar hangi tarafta?

**Yapman gerekenler:**

1. Veriyi oku ve dört sütunu al. Bir de ölçeklenmiş kopyasını hazırla.
2. Aynı ayarla (`n_clusters=4`, `random_state=42`, `n_init=10`) **iki
   kümeleme** yap: biri **ham** veride, biri ölçekli veride.
3. Her ikisi için tek satır yazdır: **ad, küme boyutları (sıralı liste),
   silüet**. İki silüeti de **ölçekli** uzayda hesapla — yoksa
   karşılaştırılamazlar.
4. Ham kümelemenin profil tablosunu yazdır (`spend` ve `visits`
   ortalamaları, bir ondalık).
5. Son satırda iki kümelemenin `adjusted_rand_score` değerini yazdır
   (üç ondalık).

**Beklenen çıktı:**

```
raw [33, 47, 95, 175] 0.202
scaled [70, 79, 99, 102] 0.517
         spend  visits
cluster
0         52.4     9.8
1        481.5    15.2
2        184.5     8.4
3        348.4    14.9
0.602
```

**Silüet 0.517'den 0.202'ye düşüyor.** Ama asıl anlatan şey boyutlar.

**Ölçekli:** 70, 79, 99, 102 — dört dengeli grup.

**Ham:** 33, 47, 95, **175**. Tek bir küme verinin yarısını yutmuş.

Profil tablosu ne olduğunu söylüyor: ham kümeleme **175 kişilik yığında
iki gerçek grubu birleştirmiş** (küme 0: harcama 52.4, ziyaret 9.8 —
birinci alıştırmadaki "nadir uğrayan" ve "sık gelen browser" gruplarının
ortalaması). Buna karşılık **yüksek harcamalıları ikiye bölmüş**: 481.5 ve
348.4. Ziyaret sayıları neredeyse aynı (15.2 ve 14.9) — yani bölme
tamamen `spend` sütununa dayanıyor.

**Sebebi tek satırda:** `spend` sütununun yayılımı 155, `returns`
sütununun 1.5. Uzaklık hesabında `spend` yüz kat ağır basıyor. Model dört
gerçek grup yerine **tek bir sütunun dört dilimini** buluyor.

**Son satır: ARI 0.602.** Küme numaraları tohuma göre değiştiği için iki
kümelemeyi etiketleriyle karşılaştıramazsın. `adjusted_rand_score` "aynı
iki kayıt aynı kümede mi" diye soruyor. 1.0 birebir aynı gruplama demek;
0.602 **gerçekten farklı iki gruplama** demek — yalnızca numaralar kaymış
değil.
