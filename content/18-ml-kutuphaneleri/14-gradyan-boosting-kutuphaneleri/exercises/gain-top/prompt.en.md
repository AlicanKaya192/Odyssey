`gain_top(k)` should return the indices of the `k` most important columns by
**gain** in the LightGBM model, from largest to smallest, as a list. The
starter code uses `feature_importances_` (the split count).

**Expected output:**

```
[15, 10, 5]
```
