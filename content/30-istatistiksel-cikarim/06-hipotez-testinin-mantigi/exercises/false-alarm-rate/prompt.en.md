`false_alarm_rate(values, n, reps, seed, alpha)` should measure the type I
error by simulation: with `np.random.default_rng(seed)` draw `reps` samples
of `n` with replacement from `values`; in each, apply `ttest_1samp` against
the true mean (the mean of `values`, so H₀ is **true**) with `axis=1`, and
return the share with `p < alpha`, with 3 places. The starter code counts
the opposite ones.

**Expected output:**

```text
0.053
0.014
```
