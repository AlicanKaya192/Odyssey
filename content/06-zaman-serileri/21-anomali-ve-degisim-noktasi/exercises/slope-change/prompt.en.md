The growth of the subscriber count slowed somewhere. Find the day and see
the effect on the forecast.

In the starter code `s` (the subscriber count), `t` (a day counter from 0) and
`y` (the values, a numpy array) are ready.

**What to do:**

1. Fit a single line to the whole series (`np.polyfit(t, y, 1)`); print the
   slope with two decimals.
2. Compute the residual of that line. Print the residual of the first day,
   the largest residual, its day (`"%m-%d"`) and the residual of the last day
   (whole numbers) on one line.
3. Look for the day of the break: for every `k` between 30 and `len(y) - 30`
   fit a separate line to each of the two pieces and add up the sums of
   squared residuals; find the `k` giving the smallest. Print the day of the
   break (`"%Y-%m-%d"`) and the two slopes (two decimals) on one line.
4. Make two forecasts for 30 days ahead (`t = len(y) - 1 + 30`): with the
   single line and with a line fitted to the last 60 days only. Print both as
   whole numbers on one line.
5. Draw a chart: the series, the single line and the two-piece line. Save it
   as `chart.png`.

**Expected output:**

```
8.98
-284 332 07-17 -356
2024-07-17 11.99 5.04
4832 4373
```

The slope of the single line (9 subscribers a day) describes neither period:
first 12, then 5. The residual being negative at the ends and positive in the
middle (an inverted V) is the signature. The difference in the forecast is
large: for a month ahead the single line says 460 subscribers too many.
