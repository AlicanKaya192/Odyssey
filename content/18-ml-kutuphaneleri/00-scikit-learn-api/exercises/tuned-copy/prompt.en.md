`tuned_copy(c)` should build `LogisticRegression(C=1.0)` and train it on the data
in the starter code. Then take a copy with `sklearn.base.clone` and change the
copy's `C` with `set_params(C=c)`. Return `[original_C, copy_C,
copy_is_fitted]`; fitted = `hasattr(copy, "coef_")`.

**Expected output:**

```
[1.0, 5.0, False]
```
