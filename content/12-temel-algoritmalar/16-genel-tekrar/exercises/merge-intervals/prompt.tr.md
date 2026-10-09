`merge_intervals(intervals)` fonksiyonunu yaz: `[başlangıç, bitiş]`
aralıklarından **çakışan ya da uç uca değenleri** birleştirsin ve sonucu
başlangıca göre sıralı döndürsün. Girdi sıralı değil.

- `[[8, 10], [1, 3], [2, 6], [15, 18]]` → `[[1, 6], [8, 10], [15, 18]]`
- `[[1, 4], [4, 5]]` → `[[1, 5]]` (4'te değiyorlar)

Önce başlangıca göre sırala (`sorted` serbest); sonra tek geçişte, son
birleştirilen aralıkla karşılaştır.

**Beklenen çıktı:**

```
[[1, 6], [8, 10], [15, 18]]
[[1, 5]]
[]
```
