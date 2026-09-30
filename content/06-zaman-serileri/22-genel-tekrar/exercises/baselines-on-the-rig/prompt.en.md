Set up the validation rig and measure three baselines: 13 origins, a 28-day
forecast at each.

`y` and `cuts` are ready in the starter code.

**What to do:**

1. Write the function `backtest(forecast)`. It takes a function of the form
   `forecast(train, index)` (returning an array of 28 values). At each cut the
   training is `y.loc[:cut]` and the test the next 28 days; the MAE is
   computed. It returns the mean MAE and the MAE of the worst experiment with
   one decimal, as a tuple.
2. Write three forecast functions:
   - `naive`: the last value of the training, 28 times
   - `seasonal_naive`: the last 7 values of the training, repeated in order
   - `week_mean`: the weekday mean of the last 28 days of the training, by the
     weekday of the test days (`index.dayofweek`)
3. Print the `backtest` result of the three, one per line.
4. Print the mean daily rentals in the test period (after 3 January 2024) as a
   whole number and the seasonal naive MAE as a percentage of that mean (a
   whole number) on one line.

**Expected output:**

```
(112.2, 234.9)
(98.6, 199.1)
(86.9, 129.7)
410 24
```

Seasonal naive is off by a quarter of an average day and its error doubles in
the worst experiment. The weekday mean of four weeks is better and far more
**stable** (worst experiment 130). In this series a single day is very noisy;
even a baseline gains by averaging. The number to beat is now 86.9.
