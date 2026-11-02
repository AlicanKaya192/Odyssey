`z_test(k_a, n_a, k_b, n_b)` should run the two-proportion z-test by hand and
return `[z, p]` (z with 3, p with 4 places): the pooled proportion, the
standard error of the difference, `z = (pB - pA) / se` and the
**two-sided** p `2 * stats.norm.sf(abs(z))`. `proportions_ztest` is not
allowed. The starter code looks at only one tail.

**Expected output:**

```text
[2.935, 0.0033]
[1.946, 0.0516]
```
