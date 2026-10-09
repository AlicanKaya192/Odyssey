`prefix_sums(values)` fonksiyonunu yaz: başında `0` olan önek toplamı
listesini döndürsün (`len(values) + 1` eleman).

- `prefix_sums([3, 1, 4])` → `[0, 3, 4, 8]`

`itertools.accumulate` ve `sum` kullanma; tek döngüde, bir öncekine ekleyerek
kur.

**Beklenen çıktı:**

```
[0, 3, 4, 8, 9, 14]
[0]
```
