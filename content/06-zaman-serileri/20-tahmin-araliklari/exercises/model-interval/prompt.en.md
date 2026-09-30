Take the interval ARIMA gives itself, read it and draw it as a band on a
chart.

In the starter code `train` (up to 5 November 2024), `test` (the next 28 days)
and the fitted model `fit` are ready.

**What to do:**

1. Take `result = fit.get_forecast(28)`. The forecast is
   `result.predicted_mean`, the 95% interval `result.conf_int(alpha=0.05)`.
2. For the first day print the forecast, the lower and upper end of the
   interval (one decimal) and the actual value on one line.
3. Print the width of the interval (upper − lower) on days 1, 7, 14 and 28
   with one decimal as a list.
4. Print the coverage of the 95% and the 80% (`alpha=0.2`) intervals over the
   test period with three decimals on one line.
5. Print the days that fall outside the interval (95%) as a `"%m-%d"` list.
6. Draw a chart: the actual values, the forecast and the 95% band with
   `ax.fill_between`. Save it as `chart.png`.

**Expected output:**

```
292.9 267.1 318.7 283
[51.6, 56.7, 65.0, 83.8]
0.964 0.893
['11-09']
```

The interval widens with the horizon: on day 28 it is more than one and a half
times as wide as on the first day. Over these 28 days the coverage is a little
above what is stated. But this is a single period; you will measure whether the
interval is really honest with 13 experiments in the next exercise.
