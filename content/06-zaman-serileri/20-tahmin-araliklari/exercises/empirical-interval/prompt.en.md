Add to the seasonal naive forecast an interval from the quantiles of its
past errors, and measure whether the interval is honest.

**What to do:**

1. Compute the one-day-ahead error: `error = s - s.shift(7)`. Separate the
   errors of 2023 as `past` and those of 2024 as `future`.
2. Print the 10% and 90% quantiles of `past` with one decimal on one line.
   These are the bounds the 80% interval adds to the forecast.
3. For 15 March 2024 print the forecast (`s.shift(7)`), the lower and upper
   end of the interval and the actual value, rounded to whole numbers, on one
   line.
4. Write the function `coverage(level)`: it takes the two quantiles of that
   level from `past` (`(1 - level) / 2` and `1 - (1 - level) / 2`) and returns
   the share of the `future` errors between those two bounds, with three
   decimals.
5. Print the results of `coverage(0.5)`, `coverage(0.8)` and `coverage(0.95)`
   on one line.

**Expected output:**

```
-21.0 23.0
288 267 311 301
0.533 0.825 0.945
```

All three intervals cover very close to what they state. You used no formula
and no distribution assumption: you only asked "how far off was this method in
the past". The interval is not symmetric (−21 and +23): the errors were not
exactly symmetric either.
