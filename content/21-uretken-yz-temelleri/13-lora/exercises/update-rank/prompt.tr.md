`update_rank(d_in, d_out, r, seed)` `np.random.default_rng(seed)` ile önce
`A = rng.normal(size=(d_in, r))`, sonra `B = rng.normal(size=(r, d_out))`
kursun ve `A @ B`'nin rankını (`np.linalg.matrix_rank`) `int` olarak
döndürsün.

**Beklenen çıktı:**

```
2
5
```
