`share_above(name, limit, n, seed)` türün ağırlıklarına normal dağılım
uydursun (ortalama `weights.mean()`, standart sapma `weights.std(ddof=1)`),
`np.random.default_rng(seed).normal(...)` ile `n` ağırlık çeksin ve iki oranı
döndürsün: `[modelde limitin üstündekilerin oranı, veride limitin
üstündekilerin oranı]`, 4 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[0.0846, 0.0605]
[0.0766, 0.0784]
```
