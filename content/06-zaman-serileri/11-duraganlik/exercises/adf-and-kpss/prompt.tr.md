İki testi fiyata ve fiyatın farkına uygula, kararı koda yazdır.

**Yapman gerekenler:**

1. `verdict(x)` adında bir fonksiyon yaz. İçinde:
   - `adf_p = adfuller(x)[1]`
   - `kpss_p = kpss(x, regression="c", nlags="auto")[1]`
   - ADF'e göre durağan: `adf_p < 0.05`. KPSS'e göre durağan:
     `kpss_p >= 0.05`.
   - İkisi de durağan diyorsa `"stationary"`, ikisi de değil diyorsa
     `"not stationary"`, aksi hâlde `"mixed"` döndür.
   Fonksiyon üç şeyi demet olarak döndürsün: `round(adf_p, 3)`,
   `round(kpss_p, 3)` ve karar metni (p-değerlerini `float(...)` ile çevir).
2. `verdict(k)` sonucunu yazdır.
3. `verdict(k.diff().dropna())` sonucunu yazdır.
4. ADF istatistiğini ve %5 kritik değerini fiyat için iki ondalığa yuvarlayıp
   aynı satıra yazdır (`result = adfuller(k)`; istatistik `result[0]`, kritik
   değerler `result[4]["5%"]`).

**Beklenen çıktı:**

```
(0.348, 0.01, 'not stationary')
(0.0, 0.1, 'stationary')
-1.87 -2.87
```

Fiyatta iki test de "durağan değil" diyor: ADF'in p-değeri büyük, KPSS'inki
küçük. Farkta ikisi de "durağan". Son satır aynı kararı başka yoldan
söylüyor: istatistik (−1.87) kritik değerden (−2.87) **daha az eksi**, yani
ret yok.
