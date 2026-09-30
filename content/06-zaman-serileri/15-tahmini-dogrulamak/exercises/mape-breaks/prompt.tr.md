`stores_long.csv` dört mağazanın 2024 satışı (`date`, `store`, `sales`).
C mağazası pazarları kapalı: o günlerin satırı yok, yani satış sıfır. Naif
tahminin hatasını A ve C mağazalarında üç ölçüyle hesapla.

Başlangıç kodunda `wide` (tarih × mağaza tablosu) hazır.

**Yapman gerekenler:**

1. A mağazasını `a`, C mağazasını `c` olarak al. C'deki boşlukları sıfırla
   doldur (`fillna(0)`). C'de kaç gün sıfır olduğunu yazdır.
2. `measures(y)` adında bir fonksiyon yaz: naif tahmin `y.shift(1)`; ilk günü
   atıp (`iloc[1:]`) üç şeyi demet olarak döndürsün: MAE (iki ondalık), MAPE
   (iki ondalık) ve MASE (iki ondalık). MASE'nin paydası bu seride
   `(y - y.shift(7)).abs().mean()` olsun.
3. `measures(a)` ve `measures(c)` sonuçlarını alt alta yazdır.
4. MAPE'nin simetrik olmadığını göster: gerçek 100 / tahmin 150 ve gerçek
   150 / tahmin 100 için yüzde hatayı bir ondalığa yuvarlayıp aynı satıra
   yazdır.

**Beklenen çıktı:**

```
52
(44.19, 13.97, 3.32)
(87.28, inf, 8.65)
50.0 33.3
```

C mağazasında MAPE `inf`: sıfır satışlı pazar günlerinde sıfıra bölünüyor.
MAE ve MASE ise iki mağazada da tanımlı ve karşılaştırılabilir. Son satır
ikinci tuzağı gösteriyor: aynı 50 birimlik ıska, tahmin yüksek olunca %50,
düşük olunca %33 sayılıyor.
