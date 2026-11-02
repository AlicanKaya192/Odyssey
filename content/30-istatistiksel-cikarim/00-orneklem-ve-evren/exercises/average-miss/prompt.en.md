`average_miss(values, n, repeats)` should measure how far the sample mean
misses the true mean on average: for each `seed` from 0 to `repeats - 1`,
pick `n` values without repeats with `np.random.default_rng(seed)`, collect
`abs(sample mean - true mean)` and return the mean of these misses with 3
places. The starter code looks at a single sample.

**Expected output:**

```text
11.873
5.34
1.678
```
