`two_processes.csv` içinde 600 günlük iki seri var (`date`, `x`, `y`). Biri
AR(1), öteki MA(1) süreciyle üretildi. Hangisinin hangisi olduğunu
korelogramlarından bul.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `w` tablosu olarak oku.
2. `x` için ACF'yi ve PACF'yi ilk 4 gecikmede iki ondalığa yuvarlayıp iki
   ayrı satırda liste olarak yazdır.
3. Aynısını `y` için yazdır.
4. `kind(series)` adında bir fonksiyon yaz: bandı `1.96 / np.sqrt(len(series))`
   alsın. **2. gecikmenin ACF'si** bandın içindeyse (ACF 1. gecikmeden sonra
   kesilmiş) `"MA"`, değilse `"AR"` döndürsün.
5. `kind(w["x"])` ve `kind(w["y"])` sonuçlarını aynı satıra yazdır.

**Beklenen çıktı:**

```
[0.69, 0.46, 0.32, 0.23]
[0.69, -0.02, 0.01, 0.03]
[0.46, -0.04, -0.04, -0.03]
[0.46, -0.31, 0.17, -0.14]
AR MA
```

`x`'te ACF adım adım sönüyor, PACF 1. gecikmeden sonra sıfır: AR. `y`'de tam
tersi: ACF 1. gecikmeden sonra sıfır, PACF işaret değiştirerek sönüyor: MA.
İkisi de katsayı 0.7 ile üretildi; aynı sayı iki süreçte çok farklı bir
hafıza veriyor.
