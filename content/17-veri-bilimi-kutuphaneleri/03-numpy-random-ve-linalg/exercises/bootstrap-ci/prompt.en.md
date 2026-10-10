`bootstrap_ci(values, n, seed)` should draw `n` bootstrap samples with
`default_rng(seed)` (a **single** `choice` call, `size=(n, len(values))`,
`replace=True`), take each row's mean and return the 2.5th and 97.5th
percentiles of the means as `[low, high]` rounded to 1 place.

**Expected output:**

```
[10.4, 13.1]
```
