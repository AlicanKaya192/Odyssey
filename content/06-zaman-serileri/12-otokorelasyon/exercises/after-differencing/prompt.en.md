Compare the correlogram of the daily sales before and after the seasonal
difference, then plot and save the one after.

**What to do:**

1. Compute `d7 = s.diff(7).dropna()`.
2. Compute the ACF of the series and of `d7` with 21 lags. For each, print on
   one line the number of lags (lag 0 excluded) whose absolute value is beyond
   the band `1.96 / np.sqrt(len(x))` (the series first).
3. Print the ACF of `d7` at lags 1, 7 and 14, rounded to two decimals, as a
   list.
4. Print the lag of `d7` with the largest absolute value and its value (two
   decimals) on one line.
5. Plot and save the correlogram of `d7`: `fig = plot_acf(d7, lags=21)`, then
   `fig.savefig("chart.png")`.

**Expected output:**

```
21 6
[0.16, -0.41, 0.02]
7 -0.41
```

In the raw series almost every lag is beyond the band: the season and the
trend fill everything. After differencing the real structure remains: a small
positive at lag 1 and a marked negative at lag 7. There is nothing at lag 14:
last week's surprise affects this week, two weeks ago does not. See the bar at
lag 7 in the **Output** tab on the left.
