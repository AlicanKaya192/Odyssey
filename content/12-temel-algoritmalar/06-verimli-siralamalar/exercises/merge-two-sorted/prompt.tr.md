`merge(left, right)` fonksiyonunu yaz: iki **sıralı** listeyi tek bir sıralı
listede birleştirsin.

İki listenin başına birer indeks (`i`, `j`) koy; küçük olanı sonuca ekleyip
o indeksi ilerlet. Liste biri bitince öbürünün kalanını ekle. Eşitlerde
**soldakini** önce al (`<=`).

`sorted` ve `.sort()` kullanma: iki listeyi uç uca ekleyip sıralamak
`O(n log n)`, birleştirmek `O(n)`.

**Beklenen çıktı:**

```
[1, 2, 3, 4, 9, 10, 12]
[5, 6]
```
