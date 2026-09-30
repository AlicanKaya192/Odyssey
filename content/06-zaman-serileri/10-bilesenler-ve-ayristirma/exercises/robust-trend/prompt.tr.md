Web trafiğinde 14 Mart 2024 bir kampanya günü: 9593 ziyaret. Klasik
ayrıştırma ile dayanıklı STL'in bu güne nasıl tepki verdiğini karşılaştır.

**Yapman gerekenler:**

1. `classic = seasonal_decompose(visits, model="additive", period=7)`.
2. `robust = STL(visits, period=7, robust=True).fit()`.
3. İki yöntemin trendindeki `NaN` sayılarını aynı satıra yazdır.
4. 14 Mart'taki trendi iki yöntem için tam sayıya yuvarlayıp aynı satıra
   yazdır (önce klasik).
5. Sıçramadan **bir gün önceki** (13 Mart) kalıntıyı iki yöntem için tam
   sayıya yuvarlayıp aynı satıra yazdır.
6. 14 Mart'ın kendi kalıntısını iki yöntem için tam sayıya yuvarlayıp aynı
   satıra yazdır.

**Beklenen çıktı:**

```
6 0
4560 3737
-1206 -136
4487 5474
```

Klasik trend sıçrama gününde 800 birim kabarıyor, çünkü 9593 yedi günün
ortalamasına giriyor. Bunun bedelini komşular ödüyor: 13 Mart, hiçbir şey
olmadığı hâlde büyük bir eksi kalıntı alıyor. Dayanıklı STL'de trend yerinde
kalıyor, komşunun kalıntısı küçük ve sıçramanın tamamı kendi gününün
kalıntısında.
