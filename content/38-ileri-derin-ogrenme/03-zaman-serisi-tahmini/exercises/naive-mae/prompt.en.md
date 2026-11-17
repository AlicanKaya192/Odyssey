`naive_mae(series, split, lag)` should treat, for every day of the test
period (`split` to the end), the value `lag` days earlier as the forecast and
return the mean absolute error with 3 places. `lag=1` is the naive, `lag=7`
the weekly seasonal naive forecast.

**Expected output:**

```
1.5
1.0
```
