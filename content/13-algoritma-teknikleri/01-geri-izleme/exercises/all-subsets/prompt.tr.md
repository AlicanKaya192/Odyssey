`subsets(items)` fonksiyonunu **geri izlemeyle** yaz: bütün alt kümeleri
derste gördüğün sırayla döndürsün (her düğümde önce şimdiki yolu ekle, sonra
sıradaki elemanlardan birini ekleyip devam et).

- `[1, 2, 3]` → `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]`

`itertools` yok.

**Beklenen çıktı:**

```
[]
[1]
[1, 2]
[1, 2, 3]
[1, 3]
[2]
[2, 3]
[3]
1024
```
