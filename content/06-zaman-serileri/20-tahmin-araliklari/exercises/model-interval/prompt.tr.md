ARIMA'nın kendi verdiği aralığı al, oku ve grafikte bant olarak çiz.

Başlangıç kodunda `train` (5 Kasım 2024'e kadar), `test` (sonraki 28 gün) ve
kurulmuş model `fit` hazır.

**Yapman gerekenler:**

1. `result = fit.get_forecast(28)` al. Tahmin `result.predicted_mean`, %95
   aralık `result.conf_int(alpha=0.05)`.
2. İlk gün için tahmini, aralığın alt ve üst ucunu (bir ondalık) ve gerçek
   değeri aynı satıra yazdır.
3. Aralığın genişliğini (üst − alt) 1., 7., 14. ve 28. günlerde bir ondalıkla
   liste olarak yazdır.
4. %95 ve %80 (`alpha=0.2`) aralıkların test dönemindeki kapsamasını üç
   ondalıkla aynı satıra yazdır.
5. Aralığın dışında kalan günleri (%95) `"%m-%d"` listesi olarak yazdır.
6. Grafik çiz: gerçek değerler, tahmin ve `ax.fill_between` ile %95 bandı.
   `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
292.9 267.1 318.7 283
[51.6, 56.7, 65.0, 83.8]
0.964 0.893
['11-09']
```

Aralık ufukla genişliyor: 28. günde ilk günün bir buçuk katından geniş. Bu
28 günde kapsama söylenenin biraz üstünde. Ama bu tek bir dönem; aralığın gerçekten
dürüst olup olmadığını bir sonraki alıştırmada 13 deneyle ölçeceksin.
