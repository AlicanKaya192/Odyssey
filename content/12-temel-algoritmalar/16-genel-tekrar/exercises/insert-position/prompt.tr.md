`insert_position(items, target)` fonksiyonunu **ikili aramayla** yaz: sıralı
listede `target`'ın sırayı bozmadan konabileceği **en soldaki** indeksi
döndürsün (`target` varsa ilk geçtiği yer).

- `[1, 3, 3, 5]`: `3` → `1`, `4` → `3`, `0` → `0`, `9` → `4`

Son satır bir milyon elemanlı listede 20 000 kez arıyor; doğrusal arama süre
sınırına takılır. `bisect` ve `index` yok.

**Beklenen çıktı:**

```
3 1
4 3
0 0
9 4
10043050000
```
