Forecast the yearly passenger total with three models: no trend, an
additive trend and a multiplicative trend.

In the starter code `annual` (the yearly totals for 2013–2024), `train`
(2013–2022) and `test` (2023–2024) are ready.

**What to do:**

1. Fit three models (all `ExponentialSmoothing(train, ...).fit()`):
   - `"flat"`: no trend
   - `"additive"`: `trend="add"`
   - `"multiplicative"`: `trend="mul"`
2. For each print the two-year forecast (`forecast(2)`) as a list rounded to
   whole numbers and the mean absolute error with one decimal, as
   `name [forecasts] MAE`, one per line.
3. Print the actual values as a list.
4. Compute the average yearly growth rate on the training data
   (`train.pct_change().mean() * 100`) and print it rounded to one decimal.

**Expected output:**

```
flat [3816, 3816] 621.5
additive [4071, 4326] 239.3
multiplicative [4233, 4690] 23.5
[4195, 4680]
10.7
```

The model with no trend stays at the last level. The additive trend adds the
same amount every year and is well behind by the second year. The
multiplicative trend grows by the same **rate** every year; since the series
grows by about 10% a year, it runs alongside the truth.
