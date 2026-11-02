`fwer(k, n, reps, seed)` should compare all pairs of `k` identical groups
(each `n` values, `rng.normal(0, 1, size=(k, n))`) with `ttest_ind` and
return, with 3 places, the share of `reps` repeats in which **at least one**
pair has `p < 0.05`. The starter code looks only at the first pair.

**Expected output:**

```text
0.222
0.046
```
