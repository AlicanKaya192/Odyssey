`welch_t(a, b)` should compute Welch's t statistic for "b minus a" by hand
and return it with 3 places: the denominator is `sqrt(va / na + vb / nb)`
(sample variances divided by `n - 1`). `ttest_ind` is not allowed. The
starter code forgot to divide the variances by the group sizes.

**Expected output:**

```text
2.109
```
