To get a forecast from a model with external variables you have to supply
their future values too. Forecast the first 28 days of November 2024.

In the starter code `train`, `test` and `columns` are ready. In this exercise
you will use `test[columns]`, that is, the **actual** values, as the future
table; we deal with that being a cheat in the next exercise.

**What to do:**

1. Fit the model with external variables (`order=(1, 0, 0)`,
   `seasonal_order=(0, 1, 1, 7)`).
2. Take the 28-day forecast: `fit.forecast(28, exog=test[columns])`.
3. Take the 28-day forecast of the model without external variables, with the
   same order.
4. Print the mean absolute error of the two forecasts with two decimals on one
   line (the one without first).
5. Print the campaign days in the test period as a `"%m-%d"` list.
6. For those days print the actual value, the forecast without and the
   forecast with variables, rounded to whole numbers, one line per day.
7. Draw a chart: the actual values (grey) and the two forecasts. Save it as
   `chart.png`.

**Expected output:**

```
17.56 11.07
['11-14', '11-15', '11-16']
285 285 294
314 286 304
243 211 223
```

The model without variables does not know a campaign is coming: on two of the
three days its forecast is about 30 units below the truth. The model with
variables adds to the days where it sees `promo = 1` in the table and catches
those two days. (On the first campaign day sales stayed below what was
expected; single days always carry noise, and the difference shows in the
average over 28 days.) On the chart you will see that only the second forecast
follows the jump on the campaign days.
