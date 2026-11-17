`shift_windows(ids, size)` dil modeli için pencere çiftleri kursun: her `i` için
girdi `ids[i:i + size]`, hedef bir adım kaydırılmışı `ids[i + 1:i + size +
1]`. `len(ids) - size` çift; `[girdiler, hedefler]` döndürsün.

**Beklenen çıktı:**

```
[[1, 2, 3], [2, 3, 4]]
[[2, 3, 4], [3, 4, 5]]
```
