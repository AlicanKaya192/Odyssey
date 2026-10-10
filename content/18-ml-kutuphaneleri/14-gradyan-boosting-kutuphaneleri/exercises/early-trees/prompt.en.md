The data has 3750 training rows; `early_stopping="auto"` stays **off** below 10,000
rows. `early_trees(rate)` should build the model with `early_stopping=True`
(a limit of 1000 trees) and return `[trees_used, test_score]` (`n_iter_`, the
score with 3 places). The starter code trains all 1000 trees.

**Expected output:**

```
[48, 0.91]
[25, 0.907]
```
