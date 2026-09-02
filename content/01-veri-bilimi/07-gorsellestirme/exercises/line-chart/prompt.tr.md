Zaman içindeki değişimi çubukla değil **çizgiyle** göstereceksin.

**Yapman gerekenler:**

1. `months` ve `sales` listeleri başlangıç kodunda hazır.
2. Ayları x, satışları y ekseninde gösteren bir **çizgi grafik** çiz;
   noktaları `marker="o"` ile işaretle.
3. Başlığı `Monthly sales` yap.
4. Y eksenini **birimiyle birlikte** `Sales (thousands)` diye etiketle.
5. Sırayla yazdır: çizgi sayısı, çizginin y verisi (liste hâlinde), y
   etiketi.

**Beklenen çıktı:**

```
1
[120, 150, 130, 180]
Sales (thousands)
```

**İki şey öğreniyorsun:**

- **Çubuk kategorileri karşılaştırıyor, çizgi bir şeyin nasıl değiştiğini
  gösteriyor.** Ayları çubukla da çizebilirsin ama eğilim çizgide daha net
  görünüyor. `marker="o"` gerçek ölçüm noktalarını işaretliyor — aradaki
  çizgi bir tahmin, noktalar veri.
- **Y etiketinde birim var:** `Sales (thousands)`. Sadece `Sales` yazsaydın
  okuyan kişi adet mi lira mı bin lira mı diye tahmin etmek zorunda
  kalırdı.
