`all_pairs(n, edges)` fonksiyonunu **Floyd–Warshall** ile yaz: düğümler
`0`..`n − 1`, kenarlar `[a, b, ağırlık]` **yönsüz**. `n × n` uzaklık
tablosunu döndürsün; ulaşılamayan çift için `-1`.

Başta `d[i][i] = 0`, kenarlar ağırlık, gerisi sonsuz. Sonra her `k` için her
`i, j`: `d[i][k] + d[k][j] < d[i][j]` ise güncelle.

**Beklenen çıktı:**

```
[0, 3, 4, -1]
[3, 0, 1, -1]
[4, 1, 0, -1]
[-1, -1, -1, 0]
```
