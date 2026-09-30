Günlük sıcaklığın mevsim normalinden sapmasına bir AR(1) modeli kur ve
tahminin nasıl ortalamaya döndüğünü gör.

Başlangıç kodunda `anomaly` (sapma serisi) hazır.

**Yapman gerekenler:**

1. Eğitim verisi 2023 sonuna kadar: `train = anomaly.loc[:"2023"]`.
   `ARIMA(train, order=(1, 0, 0)).fit()` kur.
2. AR katsayısını (`fit.params["ar.L1"]`) iki ondalıkla yazdır. Buna `phi`
   de.
3. Eğitimin son değerini ve 5 günlük tahmini iki ondalıkla aynı satıra, önce
   son değer sonra tahmin listesi olarak yazdır.
4. Aynı tahmini elle hesapla: son değeri `phi`'nin 1., 2., ..., 5. kuvvetiyle
   çarp ve iki ondalıkla liste olarak yazdır.
5. 2024'ün her günü için bir gün sonrasını üç yöntemle tahmin et ve ortalama
   mutlak hataları iki ondalıkla aynı satıra yazdır (sıra: ortalama, naif,
   AR):
   - ortalama: tahmin hep 0
   - naif: `anomaly.shift(1)`
   - AR(1): `phi * anomaly.shift(1)`

**Beklenen çıktı:**

```
0.73
3.28 [2.37, 1.7, 1.22, 0.87, 0.62]
[2.38, 1.73, 1.25, 0.91, 0.66]
1.63 1.26 1.14
```

Modelin tahmini ile elle hesap aynı: AR(1) tahmini, son sapmanın her gün `phi`
ile çarpılmış hâli. (Küçük farklar modelin sabitinden gelir; burada sıfıra çok
yakın.) Son satırda AR, iki temel yöntemin ikisinden de iyi: "sapma kalır" ile
"sapma hemen biter" arasındaki doğru cevabı veriden öğrendi.
