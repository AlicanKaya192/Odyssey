`z_test(k_a, n_a, k_b, n_b)` iki oran z-testini elle yapsın ve `[z, p]`
döndürsün (z 3, p 4 basamak): ortak oran, farkın standart hatası,
`z = (pB - pA) / se` ve **iki yönlü** p `2 * stats.norm.sf(abs(z))`.
`proportions_ztest` yasak. Başlangıç kodu tek kuyruğa bakıyor.

**Beklenen çıktı:**

```text
[2.935, 0.0033]
[1.946, 0.0516]
```
