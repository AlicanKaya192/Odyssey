`column_stats(rows)` fonksiyonunu NumPy ile yaz: `rows` iç içe liste
(satırlar örnek, sütunlar özellik). Her sütun için `[ortalama, standart sapma]`
listesini döndürsün; standart sapma `n`'e bölünür (`ddof=0`), ikisi de
`round(..., 3)`.

`np.array(rows)` ile diziye çevir, `axis=0` kullan; döngüyle toplama.

**Beklenen çıktı:**

```
55.0 11.18
3.0 0.354
```
