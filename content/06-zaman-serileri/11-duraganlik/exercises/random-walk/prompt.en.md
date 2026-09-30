Show with three measurements that the price series behaves like a random
walk.

**What to do:**

1. Print the correlation of the price with itself one day earlier (four
   decimals) and the correlation of the daily change with the previous day's
   change (three decimals) on one line.
2. Compare two simple forecasts. **The naive forecast:** tomorrow = today
   (`k.shift(1)`). **The mean forecast:** tomorrow = the mean of the last
   20 days (`k.shift(1).rolling(20).mean()`). Put both and the actual value
   in one table, use `dropna()` to keep the days where both are defined, and
   print the mean absolute error of each forecast, rounded to two decimals,
   on one line (naive first).
3. Compute the share of up days (`(change > 0).mean()`). Then compute the
   same share only on days **whose previous day was an up day**. Print both,
   rounded to three decimals, on one line.

**Expected output:**

```
0.9927 0.041
1.84 5.36
0.529 0.53
```

The level carries yesterday over almost exactly, while the changes are
unrelated. The naive forecast is clearly better than the 20-day mean: in a
random walk the freshest information is the last value. And the fact that it
rose yesterday barely changes the chance that it rises today.
