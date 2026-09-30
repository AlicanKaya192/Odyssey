Put Holt–Winters through the rig of Section 15: 13 origins, a 28-day
horizon, against seasonal naive.

In the starter code `snaive(train, h)`, `cuts` (the 13 cut days) and
`backtest(forecast)` are ready: `backtest` returns the MAEs of the given
forecast function over the 13 experiments as a numpy array.

**What to do:**

1. Write the function `hw(train, h)`: it fits the model with no trend and an
   additive season (`seasonal_periods=7`) on `train` and returns the `h`-day
   forecast as a numpy array (`.forecast(h).to_numpy()`).
2. Write the function `hw_trend(train, h)`: the same, with `trend="add"`.
3. Put the three methods through `backtest`. For each print the mean MAE and
   the worst experiment with two decimals as `name mean worst`, one per line
   (names: `snaive`, `hw`, `hw trend`).
4. Compute the difference of `hw` from seasonal naive experiment by experiment
   (`snaive − hw`): print its mean, its standard deviation (`ddof=1`, two
   decimals) and the number of experiments `hw` wins on one line.
5. Print the skill of `hw` (`1 - mean_hw / mean_snaive`) with two decimals.

**Expected output:**

```
snaive 17.95 41.29
hw 15.91 38.57
hw trend 16.81 51.26
2.04 1.85 12
0.11
```

The model with no trend is ahead in 12 of the 13 experiments: the difference
is small but **consistent**. Adding a trend does not improve the mean and
makes the worst experiment markedly worse: the trend carries the year-end rise
into January. For this series the right choice is the model with fewer
components; its gain is 11%.
