`sort_by_score(records)` fonksiyonunu merge sort ile yaz: `[ad, puan]`
çiftlerini **puana göre artan** sıralasın; puanı eşit olanlar **girdideki
sıralarını korusun** (kararlı).

- `[["Bora", 2], ["Ada", 2], ["Cem", 1]]` →
  `[["Cem", 1], ["Bora", 2], ["Ada", 2]]` (Bora girdide Ada'dan önceydi)

Birleştirmede puanları karşılaştır (`left[i][1] <= right[j][1]`); `<=`
kararlılığı sağlıyor. `sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
[['Cem', 1], ['Bora', 2], ['Ada', 2]]
[['y', 3], ['w', 3], ['x', 5], ['z', 5]]
```
