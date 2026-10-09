`flatten(items)` fonksiyonunu **özyinelemeyle** yaz: ne kadar iç içe olursa
olsun bir listedeki bütün sayıları, **soldan sağa sırayla**, düz bir listede
döndürsün.

- `flatten([1, [2, 3], [4, [5, [6]]]])` → `[1, 2, 3, 4, 5, 6]`
- `flatten([[], [[]]])` → `[]`

Elemanları gezmek için `for` kullanabilirsin; ama alt listeler için
fonksiyon **kendini çağırmalı**. Bir değerin liste olup olmadığını
`isinstance(item, list)` söyler.

**Beklenen çıktı:**

```
[1, 2, 3, 4, 5, 6]
[]
```
