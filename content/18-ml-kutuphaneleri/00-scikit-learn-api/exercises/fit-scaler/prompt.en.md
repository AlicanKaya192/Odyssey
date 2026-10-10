`fit_scaler(train, test)` should fit a `StandardScaler` on the **training** data
only and transform the test data with it. Return `[means, test]`: `mean_`
with 3 places, the transformed test as a list of lists with 2 places. The
starter code joins the two and fits on that: leakage.

**Expected output:**

```
[[2.0, 20.0], [[0.0, 3.0]]]
```
