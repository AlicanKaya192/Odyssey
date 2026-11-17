`split_sizes(n, val_fraction, seed)` `range(n)`'i `random_split` ile eğitim
ve doğrulama olarak bölsün: doğrulama `int(n * val_fraction)` örnek, üreteç
`torch.Generator().manual_seed(seed)`. `[eğitim boyu, doğrulama boyu,
doğrulamadaki en küçük üç numara]` döndürsün (`val.indices`).

**Beklenen çıktı:**

```
[48, 12, [5, 10, 13]]
[7, 3, [3, 4, 7]]
```
