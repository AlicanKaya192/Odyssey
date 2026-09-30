Beat the baseline (86.9): build a linear model from calendar features known
in the future and measure where the rest of the error comes from.

In the starter code `features(index)` (trend, weekday, yearly Fourier,
holiday) and `backtest(forecast)` are ready.

**What to do:**

1. `log_model(train, index)`: fit a `LinearRegression` on
   `features(train.index)` and `np.log(train)`; return the forecast for
   `index` turned back to levels with `np.exp`. Print the `backtest` result.
2. `level_model(train, index)`: the same, without the logarithm. Print the
   result.
3. `weather_model(train, index)`: the same as `log_model`, but add the weather
   **that occurred** to the features: `features(...).join(weather)`. Print the
   result.
4. Fit the model with weather features once on the whole series. Print the
   `np.exp` of the `rain` and `holiday` coefficients with two decimals on one
   line (the effect as a multiplier).
5. Print, as a whole number, by what percentage the mean MAE of `log_model` is
   lower than the four-week weekday mean (86.9).

**Expected output:**

```
(65.1, 95.9)
(67.6, 104.7)
(20.9, 31.3)
0.62 1.14
25
```

The calendar model beats the baseline by a quarter; fitting on the logarithm
improves both the mean and the worst experiment. The third line is not a model
but a **limit**: the weather of the test days is not known when forecasting.
But it shows where the remaining error comes from: a rainy day cuts rentals to
0.62 times, and the model does not know which day will be rainy.
