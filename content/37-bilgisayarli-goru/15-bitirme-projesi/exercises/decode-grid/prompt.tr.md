`decode_grid(output, S, size, threshold)` `S × S` hücrenin her birinde
`[nesnellik, kx, ky, w, h, p0, p1, ...]` olasılıklarını alıp güveni
(nesnellik × en büyük olasılık) eşikten küçük olmayan hücreleri
`[x1, y1, x2, y2, sınıf, güven]` kutularına çevirsin (güven 2 basamak;
satır satır, soldan sağa).

**Beklenen çıktı:**

```
[8.0, 0.0, 16.0, 8.0, 1, 0.81]
[0.0, 12.0, 4.0, 16.0, 0, 0.42]
[8.0, 8.0, 16.0, 16.0, 0, 0.4]
```
