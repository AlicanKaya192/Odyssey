`predict_one(xs, ys, x)` should train a `LinearRegression` on single-feature
data (`xs`, `ys`) and return the prediction for `x` as a `float` rounded to 2
places. Both the training data and the prediction input must be
**two-dimensional**: `np.array(xs).reshape(-1, 1)` and `[[x]]`. The starter
code passes one-dimensional data and stops.

**Expected output:**

```
21.0
```
