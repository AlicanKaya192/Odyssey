The true values of the 8 missing days sit in `store_sales.csv`. Try four
filling methods and measure how close each gets to the truth.

In the starter code `full` (the 2024 series with the gaps as `NaN`) and
`truth` (the real sales) are ready.

**What to do:**

1. Take the index of the missing days: `days = full[full.isna()].index`.
2. Write a function `score(filled)`: it returns the mean absolute difference
   between the values of the filled series on the missing days and the true
   values, rounded to one decimal.
3. Apply four methods and print them as `name error`, one per line:
   - `ffill`: `full.ffill()`
   - `linear`: `full.interpolate()`
   - `week ago`: `full.fillna(full.shift(7))`
   - `both sides`: the average of a week before and a week after
     (`pd.concat([full.shift(7), full.shift(-7)], axis=1).mean(axis=1)`)
4. For 10 February print the true value and the value written by the four
   methods, rounded to whole numbers, on one line (order: truth, ffill,
   linear, week ago, both sides).

**Expected output:**

```
ffill 45.0
linear 46.1
week ago 9.8
both sides 7.0
388 302 276 389 382
```

The two methods that use the weekly pattern are five times more accurate than
those that do not. The last line shows why: 10 February is a Saturday; `ffill`
and linear filling write a number at the weekday level.
