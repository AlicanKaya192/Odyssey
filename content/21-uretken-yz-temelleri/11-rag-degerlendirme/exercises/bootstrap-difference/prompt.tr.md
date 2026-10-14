`bootstrap(a, b, n, seed)` iki ayarın soru başına doğru (1) / yanlış (0)
listelerini alsın. `rng = np.random.default_rng(seed)` ile `n` kez
`pick = rng.integers(0, len(a), len(a))` çekip `a[pick].sum() - b[pick].sum()`
farkını hesaplasın. Döndür: `[gözlenen fark, %5'lik değer, %95'lik değer]`;
yüzdelikler `np.percentile` ile, 1 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[2, 0.0, 4.0]
```
