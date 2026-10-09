`minibatch_epoch(A, y, w, lr, batch, seed)` fonksiyonunu yaz: bir epoch
mini-batch gradyan inişi. Sıra `np.random.default_rng(seed).permutation(n)`;
`0, batch, 2·batch, …` başlangıçlarından grupları al, her grupta o grubun MSE
gradyanıyla (`2/len(grup)`) bir adım at. `.round(4).tolist()` döndürsün.

**Beklenen çıktı:**

```
[0.5286, 3.0044]
[0.5863, 3.2303]
[0.6083, 3.2057]
```
