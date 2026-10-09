`two_opt_length(pts, tour)` fonksiyonunu yaz: turu 2-opt ile iyileştirip
son turun uzunluğunu `round(..., 1)` ile döndürsün.

Döngü dersteki gibi: `i` `1..n−2`, `j` `i+1..n−1`; iyileşme varsa
`tour[i:j + 1]`'i hemen ters çevir ve taramaya devam et; bir tam turda
iyileşme yoksa dur. **Hız:** turu her denemede baştan ölçme;
`a, b, c, d = tour[i-1], tour[i], tour[j], tour[(j+1) % n]` için yalnızca
`dist(a, c) + dist(b, d) − dist(a, b) − dist(c, d)` farkına bak
(`< -1e-9` ise iyileşme). Son satırda 300 şehir var.

**Beklenen çıktı:**

```
14.0
1521.7
```
