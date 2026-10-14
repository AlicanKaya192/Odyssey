`train_linear(k, steps, lr, seed)` doğrusal bir otomatik kodlayıcıyı gradyan
inişiyle eğitsin. `A = X_train - mean`; üreteç `np.random.default_rng(seed)` ile
önce `E = rng.normal(0, 0.1, (64, k))`, sonra `D = rng.normal(0, 0.1, (k, 64))`.
Her adımda: `code = A @ E`, `err = code @ D - A`,
`gD = code.T @ err * 2 / err.size`, `gE = A.T @ (err @ D.T) * 2 / err.size`,
sonra `E -= lr * gE` ve `D -= lr * gD`. Sonunda test resimlerinin hatasını
(`(X_test - mean) @ E @ D + mean` ile geri kurup) 4 basamağa yuvarlanmış
`float` olarak döndür.

**Beklenen çıktı:**

```
0.0248
0.0245
```
