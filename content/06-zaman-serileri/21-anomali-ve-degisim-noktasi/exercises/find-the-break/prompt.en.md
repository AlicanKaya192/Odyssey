Find in hindsight the day the level changed and measure how cleaning the
series strengthens the evidence.

**What to do:**

1. Write the function `best_split(x, margin=14)`: it turns `x` into a numpy
   array; for every `k` between `margin` and `len(x) - margin` it computes the
   sum of squared deviations of the two pieces from their own means; it
   returns the `k` giving the smallest and the gain
   (`1 - smallest sum / sum of squares of the whole series`).
2. On the raw series (`v`) print the day of the change (`"%Y-%m-%d"`) and the
   gain (two decimals).
3. Remove the weekend effect: `ratio` is the median of the weekend days over
   the median of the weekdays (print it with three decimals). `adjusted` is
   the series with the weekend values divided by `ratio`. Print the day of the
   change and the gain.
4. Repair the three anomaly days as well: in a copy of `adjusted` make 14
   March, 20 June and 8 October `NaN` and fill them with `interpolate()`
   (`clean`). Print the day of the change, the gain, the mean before and after
   (whole numbers) and the percentage change (a whole number) on one line.
5. Apply `best_split` again to the two pieces of `clean`; print the two gains
   with three decimals on one line.

**Expected output:**

```
2024-09-02 0.3
0.723
2024-09-02 0.52
2024-09-02 0.88 4004 5235 31
0.013 0.015
```

The same day is found in all three attempts, but the gain goes from 0.30 to
0.88: with the weekly pattern and the anomalies removed the level shift is
almost all of the movement. There is no second change inside the two pieces:
the gain is one or two per cent. `best_split` always returns a day; the
decision is made from the gain.
