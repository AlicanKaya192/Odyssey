`load_scores(rows)` fonksiyonunu yaz: bellekte `scores (name, score)`
tablosunu kursun, `rows`'u **`executemany`** ile eklesin ve tek bir sorguyla
`[satır sayısı, ortalama puan]` listesini döndürsün; ortalama SQL'de
`ROUND(AVG(score), 1)` ile yuvarlansın. Boş listede ortalama `None` olur.

**Beklenen çıktı:**

```
[3, 82.3]
```
