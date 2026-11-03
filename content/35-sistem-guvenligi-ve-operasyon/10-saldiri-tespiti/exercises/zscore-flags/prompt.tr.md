`zscore_flags(baseline, values, limit)` temel çizginin ortalamasını ve
standart sapmasını (`statistics.mean`, `statistics.stdev`) alsın;
`values`'tan z skorunun mutlak değeri `limit`'ten **büyük** olanları
sırasıyla döndürsün. Sapma 0 ise (bütün temel değerler aynı) ortalamaya
eşit olmayan her değer işaretlensin.

**Beklenen çıktı:**

```
[410, 100, 140]
[6]
```
