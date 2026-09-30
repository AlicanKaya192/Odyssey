Compare four seasonal ARIMA candidates for the daily sales on three
criteria: the AIC, the residual test and the test error.

In the starter code `train`, `test` and `candidates` (four pairs of orders)
are ready.

**What to do:**

1. For each candidate fit the model
   (`ARIMA(train, order=order, seasonal_order=seasonal).fit()`) and compute:
   - the AIC (one decimal)
   - the Ljung–Box p-value: drop the first 8 values of the residual, 14 lags
     (three decimals)
   - the mean absolute error of the 28-day forecast (two decimals)
2. For each candidate print a line as `order seasonal AIC p MAE`.
3. Print the order of the candidate with the smallest AIC.
4. Print the orders of the candidates whose Ljung–Box p-value is above 0.05 as
   a list.

**Expected output:**

```
(0, 0, 0) (0, 1, 0, 7) 8782.5 0.0 11.64
(1, 0, 0) (0, 1, 1, 7) 8423.1 0.0 14.9
(0, 1, 1) (0, 1, 1, 7) 8265.8 0.035 10.48
(1, 1, 1) (0, 1, 1, 7) 8258.7 0.311 10.44
(1, 1, 1)
[(1, 1, 1)]
```

The first line is seasonal naive written as an ARIMA: a seasonal difference
only. The second candidate is far better on AIC, yet its test error is worse
and there is memory in its residual: the AIC alone is not enough. Only the
last candidate meets all three criteria at once: the smallest AIC, a clean
residual, the smallest test error.
