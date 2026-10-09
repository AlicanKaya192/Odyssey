`distinct_estimate(items, p)` fonksiyonunu **HyperLogLog** ile yaz.
`m = 2 ** p` kova. Her öğe için `v = h(item, 0)`; kova `v & (m - 1)`;
`rest = v >> p`; sıra `rank = (64 - p) - rest.bit_length() + 1`; kovanın
değeri şimdiye kadarki en büyük `rank`.

Kovalar dolunca tahmin formülü başlangıç kodunda hazır.

**Beklenen çıktı:**

```
100 108
5000 4949
40000 36206
```
