Fit a seasonal model to the daily sales, read its components and see its
forecast on a chart.

In the starter code `train` (up to 5 November 2024) and `test` (the next
28 days) are ready.

**What to do:**

1. Fit the model with no trend and an additive season:
   `ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()`.
2. Print the coefficients `α` and `γ` (`smoothing_level`,
   `smoothing_seasonal`) with two decimals on one line.
3. Print the last level (`fit.level.iloc[-1]`) with one decimal.
4. Print the last 7 seasonal shares (`fit.season.iloc[-7:]`) with one decimal
   as a list. (Order: Wednesday to Tuesday.)
5. Take the 28-day forecast and print its first 7 days with one decimal as a
   list.
6. Print the mean absolute error and the bias of the forecast with two
   decimals on one line.
7. Draw a chart: the last 28 days of training and the test (grey), with the
   forecast on top. Save it as `chart.png`.

**Expected output:**

```
0.18 0.13
314.0
[-23.2, -11.1, 35.3, 96.0, 48.3, -39.3, -41.3]
[290.8, 302.9, 349.3, 410.0, 362.3, 274.7, 273.8]
11.73 7.68
```

The first week of the forecast is the last level plus that day's seasonal
share: the fourth value (Saturday) is 314.0 + 96.0. The bias is positive: the
forecast is a little low on average, because the model carries no trend and
sales rise at the end of November. On the chart you will see the forecast
repeating the same seven numbers every week.
