Günlük satışı 7 günlük hareketli ortalamayla düzleştir.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. 7 günlük hareketli ortalamayı hesapla: `s.rolling(7).mean()`.
3. Baştaki `NaN` sayısını yazdır.
4. 10 Mart 2024 (pazar) için hareketli ortalamayı ve 4–10 Mart haftasının
   ortalamasını bir ondalığa yuvarlayıp aynı satıra yazdır.
5. Ham serinin ve hareketli ortalamanın standart sapmasını bir ondalığa
   yuvarlayıp aynı satıra yazdır.
6. 9 Mart 2024 için üstel ağırlıklı ortalamayı (`s.ewm(span=7).mean()`) ve
   hareketli ortalamayı bir ondalığa yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
6
282.6 282.6
58.9 39.1
299.2 283.7
```

Dördüncü adımda iki sayı aynı: pazar günündeki 7 günlük ortalama, o gün biten
haftanın ortalaması. Son satırda `ewm` daha yüksek, çünkü en yeni güne
(yüksek satışlı cumartesi) daha çok ağırlık veriyor.
