`windows(text, size, overlap)` metni kelimelere bölüp `size` kelimelik
parçalar döndürsün; ardışık parçalar `overlap` kelime örtüşsün (adım
`size - overlap`). Başlangıç konumları `range(0, max(len(words) - overlap, 1),
size - overlap)`; her parça kelimelerin boşlukla birleşimi.

**Beklenen çıktı:**

```
a b c d
d e f g
g h i j
```
