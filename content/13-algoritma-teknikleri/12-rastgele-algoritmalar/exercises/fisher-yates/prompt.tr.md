`shuffled(items, seed)` fonksiyonunu yaz: listenin karıştırılmış bir
**kopyasını** döndürsün; asıl liste değişmesin. Üreteç `rng = random.Random(seed)`.

Fisher-Yates: `i`'yi sondan `1`'e kadar indir; `j = rng.randint(0, i)` ve
`i` ile `j`'yi değiştir. (Aynı çıktı için sıra ve aralık tam böyle olmalı.)
`shuffle` ve `sample` yok.

**Beklenen çıktı:**

```
[3, 4, 5, 1, 2]
[3, 2, 4, 5, 1]
['c', 'a', 'b']
```
