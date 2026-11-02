`efficiency_ratio(values, n, reps, seed)` should measure how many times
more data the median needs than the mean: with `np.random.default_rng(seed)`
draw `reps` samples of `n` people with replacement, find the standard
deviations of the means and of the medians and return the ratio of the
**variances**, that is `(sd_median / sd_mean) ** 2`, with 2 places. The
starter code does not square.

**Expected output:**

```text
2.69
```
