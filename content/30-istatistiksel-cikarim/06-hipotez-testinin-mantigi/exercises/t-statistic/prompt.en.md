`t_stat(values, mu0)` should compute the one-sample t statistic by hand:
`(mean - mu0) / (s / sqrt(n))`, where `s` is the sample standard deviation
(divided by `n - 1`). Return it with 3 places. `ttest_1samp` is not allowed.
The starter code uses `n` instead of `sqrt(n)` in the denominator.

**Expected output:**

```text
3.667
1.414
```
