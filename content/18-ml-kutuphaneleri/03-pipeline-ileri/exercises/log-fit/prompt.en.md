`log_fit(xs, ys, x)` should chain `FunctionTransformer(np.log10)` and
`LinearRegression` with `make_pipeline`, train on the single-feature data
(`xs` → a column) and return the prediction for `x` as a `float` rounded to 2
places.

**Expected output:**

```
5.0
```
