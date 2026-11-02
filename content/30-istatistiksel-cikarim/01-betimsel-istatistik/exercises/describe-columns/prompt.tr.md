`load_ms` ve `minutes` sütunlarının her biri için tek satırda sütun adını,
ortalamayı, medyanı, standart sapmayı (pandas `std()`) ve 95. yüzdeliği
(`np.percentile(x, 95)`) yazdır, hepsi 1 basamak. Son satıra ortalama ile
medyanı en çok ayrışan (farkın mutlak değeri en büyük) sütunun adını yaz.

**Beklenen çıktı:**

```text
load_ms 849.7 850.0 120.3 1048.0
minutes 9.0 7.5 6.1 20.5
minutes
```
