`nan_forest(rate)` turns a `rate` fraction of the training cells into `NaN`. Since
a random forest accepts `NaN` directly, it should train **without filling**
these gaps and return the test score (3 places). The starter code fills the
gaps with 0 (`np.nan_to_num`).

**Expected output:**

```
0.9
0.893
```
