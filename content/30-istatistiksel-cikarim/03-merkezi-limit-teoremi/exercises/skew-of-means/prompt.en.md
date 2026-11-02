`skew_of_means(values, n, reps, seed)` should draw `reps` samples of `n`
people with replacement from `values`
(`np.random.default_rng(seed).choice(values, size=(reps, n))`), take the row
means and return the skewness of **the means** (`scipy.stats.skew`) with 2
places. The starter code returns the skewness of the data itself.

**Expected output:**

```text
1.7
0.39
```
