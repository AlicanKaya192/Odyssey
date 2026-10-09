`merge_sorted(lists)` fonksiyonunu **heap ile** yaz: her biri küçükten büyüğe
sıralı listeleri tek bir sıralı listede birleştirsin.

1. Her boş olmayan listenin ilk elemanını `(değer, liste_no, indeks)` olarak
   heap'e koy.
2. En küçüğü al, sonuca ekle; o listenin **bir sonraki** elemanı varsa heap'e
   koy.
3. Heap boşalınca bitti.

`sorted`, `sort` ve `heapq.merge` yok.

**Beklenen çıktı:**

```
[1, 2, 3, 4, 5, 9, 10]
[1, 1, 7]
```
