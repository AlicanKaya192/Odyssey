`permutations(items)` fonksiyonunu **geri izlemeyle** yaz: listenin bütün
sıralanışlarını liste listesi olarak döndürsün. Sıra: her adımda kullanılmamış
elemanları **listedeki sırasıyla** dene.

- `[1, 2, 3]` → `[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]`

Kullanılanları `used` listesinde işaretle; geri alırken işareti kaldırmayı
unutma. `itertools` yok.

**Beklenen çıktı:**

```
[1, 2, 3]
[1, 3, 2]
[2, 1, 3]
[2, 3, 1]
[3, 1, 2]
[3, 2, 1]
5040
```
