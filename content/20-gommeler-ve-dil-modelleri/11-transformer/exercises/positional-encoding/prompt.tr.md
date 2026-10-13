`positional_encoding(n, d)` dersteki sinüs kodlamasını kursun: her `pos` için
`i = 0, 2, 4, ...` adımlarında `açı = pos / 10000 ** (i / d)`; satıra önce
`sin(açı)`, sonra `cos(açı)` eklensin. 3 basamak.

**Beklenen çıktı:**

```
[0.0, 1.0, 0.0, 1.0]
[0.841, 0.54, 0.01, 1.0]
[0.909, -0.416, 0.02, 1.0]
```
