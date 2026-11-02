`sample_mean(values, n, seed)` should pick `n` values from `values`
**without repeats** and return their mean with 2 places. To pick, use
`np.random.default_rng(seed).choice(values, size=n, replace=False)`. The
starter code returns the mean of the whole list (the parameter); the
sample's mean (a statistic) is wanted.

**Expected output:**

```text
9.6
10.2
10.5
```
