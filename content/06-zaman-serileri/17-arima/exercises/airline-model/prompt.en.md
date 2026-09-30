Fit a seasonal ARIMA to the monthly passenger series: the logarithm, one
difference, one seasonal difference, one MA term of each kind. Forecast 2024
and save a chart.

In the starter code `train` (up to the end of 2023) and `test` (2024) are
ready.

**What to do:**

1. Fit the model on the logarithm:
   `ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()`.
2. Print the two MA coefficients (`ma.L1`, `ma.S.L12`) with two decimals on
   one line.
3. Take the 12-month forecast and turn it back with `np.exp`. Print the mean
   absolute error (two decimals) and the percentage error (one decimal) on one
   line.
4. Fit the same model **without** the logarithm and print its mean absolute
   error with two decimals.
5. A residual check: drop the first 13 values of the residual of the log
   model (`fit.resid.iloc[13:]`) and print the Ljung–Box p-value at 12 lags
   with two decimals.
6. Print the forecast for August 2024 and the actual value, rounded to whole
   numbers, on one line.
7. Draw a chart: the actual values for 2022–2024 and the forecast of 2024.
   Save it as `chart.png`.

**Expected output:**

```
-0.94 -0.95
6.14 1.6
11.05
0.99
493 480
```

A model with two coefficients forecasts the twelve months with a mean error of
1.6%, and no memory is left in its residual (a large p-value). Without the
logarithm the error almost doubles: the transformation is part of the model.
The bar from Section 14 was 11.11 and Holt–Winters 6.53.
