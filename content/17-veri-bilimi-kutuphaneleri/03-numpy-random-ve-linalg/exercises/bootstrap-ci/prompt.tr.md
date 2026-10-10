`bootstrap_ci(values, n, seed)` `default_rng(seed)` ile `n` bootstrap
örneklemi çeksin (**tek** `choice` çağrısı, `size=(n, len(values))`,
`replace=True`), her satırın ortalamasını alsın ve ortalamaların 2,5 ile
97,5 yüzdeliklerini 1 basamağa yuvarlı `[alt, üst]` olarak döndürsün.

**Beklenen çıktı:**

```
[10.4, 13.1]
```
