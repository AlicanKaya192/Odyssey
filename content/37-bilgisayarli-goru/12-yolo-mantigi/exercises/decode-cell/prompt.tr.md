`decode_cell(row, col, values, S, size)` bir hücrenin `values` listesini
(`[nesnellik, kx, ky, w, h, p0, p1, ...]`) kutuya çevirsin:
`[x1, y1, x2, y2, sınıf, güven]`. Sınıf en büyük olasılığın sırası, güven
nesnellik × o olasılık (2 basamak).

**Beklenen çıktı:**

```
[16.0, 4.0, 24.0, 20.0, 1, 0.8]
[0.0, 4.0, 4.0, 8.0, 2, 0.5]
```
