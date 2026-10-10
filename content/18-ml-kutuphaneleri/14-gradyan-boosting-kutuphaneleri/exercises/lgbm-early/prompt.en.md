`lgbm_early(patience)` should train LightGBM with the validation part
(`eval_X=X_val`, `eval_y=y_val`) and the `lgb.early_stopping(patience,
verbose=False)` callback, and return `[best_iteration_, test_score]` (the
score with 3 places). `eval_set` is deprecated in this version; do not use
it. The starter code trains all 2000 trees.

**Expected output:**

```
[57, 0.828]
[57, 0.828]
```
