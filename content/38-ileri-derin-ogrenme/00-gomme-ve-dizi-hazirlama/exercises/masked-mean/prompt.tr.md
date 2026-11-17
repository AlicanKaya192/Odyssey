`masked_mean(vectors, mask)`: `vectors` `(B, T, D)`, `mask` `(B, T)` (1 gerçek,
0 dolgu). Her dizi için yalnızca gerçek konumların vektörlerinin
ortalamasını alsın ve `(B, D)` sonucu 3 basamakla liste olarak döndürsün.

**Beklenen çıktı:**

```
[[2.0, 3.0], [2.0, 2.0]]
```
