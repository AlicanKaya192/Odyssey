`sample_stats(mu, logvar, n, seed)` yeniden parametrelendirme hilesiyle `n`
kod çeksin: `std = np.exp(0.5 * logvar)`,
`z = mu + std * rng.normal(size=(n, len(mu)))`, üreteç
`np.random.default_rng(seed)`. Önce her boyutun ortalamasını, sonra
standart sapmasını içeren tek bir liste döndürsün; her sayı 2 basamağa
yuvarlanmış `float`.

**Beklenen çıktı:**

```
[1.5, -0.5, 0.37, 1.0]
[0.01, 1.66]
```
