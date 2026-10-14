`update_rank(d_in, d_out, r, seed)` should build first
`A = rng.normal(size=(d_in, r))`, then `B = rng.normal(size=(r, d_out))` with
`np.random.default_rng(seed)` and return the rank of `A @ B`
(`np.linalg.matrix_rank`) as an `int`.

**Expected output:**

```
2
5
```
