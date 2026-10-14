`histogram_sample(name, bins, n, seed)` türün ağırlıklarının histogramından
(`np.histogram(weights, bins=bins)`) `n` örnek üretsin: üreteç
`g = np.random.default_rng(seed)`; kutu `g.choice(len(p), size=n, p=p)` ile,
değer `g.uniform(edges[box], edges[box + 1])` ile. `[ortalama, standart
sapma]` döndür, 1 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[552.1, 106.6]
[306.8, 71.1]
```
