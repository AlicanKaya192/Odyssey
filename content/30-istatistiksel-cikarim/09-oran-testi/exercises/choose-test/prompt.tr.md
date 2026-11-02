`choose_test(k_a, n_a, k_b, n_b)` önce H₀ altındaki beklenen sayılara baksın:
ortak oran `pool` ile `n_a * pool`, `n_a * (1 - pool)`, `n_b * pool`,
`n_b * (1 - pool)`. Biri 5'in altındaysa `["fisher", p]`, değilse z-testiyle
(`proportions_ztest([k_b, k_a], [n_b, n_a])`) `["z", p]` döndürsün (p 4
basamak). Başlangıç kodu hep z-testi yapıyor.

**Beklenen çıktı:**

```text
['z', 0.0033]
['z', 0.0186]
```
