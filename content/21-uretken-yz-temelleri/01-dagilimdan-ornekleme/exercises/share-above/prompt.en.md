`share_above(name, limit, n, seed)` should fit a normal distribution to the
species' weights (mean `weights.mean()`, standard deviation
`weights.std(ddof=1)`), draw `n` weights with
`np.random.default_rng(seed).normal(...)` and return two shares:
`[share above the limit in the model, share above the limit in the data]`,
as `float`s rounded to 4 places.

**Expected output:**

```
[0.0846, 0.0605]
[0.0766, 0.0784]
```
