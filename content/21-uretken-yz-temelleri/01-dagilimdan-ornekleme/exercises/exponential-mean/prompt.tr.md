`exponential_mean(rate, n, seed)` ters dönüşümle `n` üstel bekleme süresi
üretsin (`t = -log(1 - u) / rate`) ve ortalamalarını 3 basamağa yuvarlanmış
`float` olarak döndürsün. Düzgün sayılar
`np.random.default_rng(seed).random(n)`.

**Beklenen çıktı:**

```
2.014
0.498
```
