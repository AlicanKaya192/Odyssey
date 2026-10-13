- `minhash(items, num)`: `seed` 0'dan `num - 1`'e kadar her tohum için
  öğelerin `zlib.crc32(f"{seed}:{item}".encode())` değerlerinin **en
  küçüğünü** alsın; `num` sayılık liste döndürsün.
- `estimate(sig_a, sig_b)`: aynı sıradaki eşit sayıların oranı, 3 basamak.

**Beklenen çıktı:**

```
1058669311
137461500
143626334
250746978
0.75
```
