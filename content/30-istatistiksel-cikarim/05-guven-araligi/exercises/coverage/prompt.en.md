`coverage(values, n, reps, seed, level)` should measure whether the interval
method keeps its promise: with `np.random.default_rng(seed)` draw `reps`
samples of `n` people with replacement, build a t interval at confidence
`level` for each and return the share that catch the true mean of `values`,
with 3 places. The starter code always uses 1.96: wrong both for small
samples and for 90%.

**Expected output:**

```text
0.937
0.904
```
