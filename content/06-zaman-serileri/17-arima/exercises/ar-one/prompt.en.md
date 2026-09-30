Fit an AR(1) model to the deviation of the daily temperature from the
seasonal normal and see how the forecast returns to the mean.

`anomaly` (the deviation series) is ready in the starter code.

**What to do:**

1. The training data goes up to the end of 2023:
   `train = anomaly.loc[:"2023"]`. Fit `ARIMA(train, order=(1, 0, 0)).fit()`.
2. Print the AR coefficient (`fit.params["ar.L1"]`) with two decimals. Call it
   `phi`.
3. Print the last training value and the 5-day forecast with two decimals on
   one line, the last value first and then the forecast as a list.
4. Compute the same forecast by hand: multiply the last value by the 1st, 2nd,
   ..., 5th power of `phi` and print the results with two decimals as a list.
5. For every day of 2024 forecast one day ahead with three methods and print
   the mean absolute errors with two decimals on one line (order: mean, naive,
   AR):
   - mean: the forecast is always 0
   - naive: `anomaly.shift(1)`
   - AR(1): `phi * anomaly.shift(1)`

**Expected output:**

```
0.73
3.28 [2.37, 1.7, 1.22, 0.87, 0.62]
[2.38, 1.73, 1.25, 0.91, 0.66]
1.63 1.26 1.14
```

The model's forecast and the hand calculation agree: an AR(1) forecast is the
last deviation multiplied by `phi` each day. (Small differences come from the
constant of the model, which is very close to zero here.) On the last line AR
beats both baselines: it learnt from the data the right answer between "the
deviation stays" and "the deviation ends at once".
