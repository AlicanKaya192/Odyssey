How should the interval of the naive forecast of the share price widen with
the horizon? Compare the square root rule with a constant width.

**What to do:**

1. Compute the standard deviation of the daily change: `sd = k.diff().std()`;
   print it with three decimals.
2. Starting from the last value of the series, print the 95% interval
   (`last ± 1.96 * sd * sqrt(h)`) for `h = 1, 10, 40` with one decimal as
   `h lower upper`, one per line.
3. Write the function `coverage(h, widen)`: starting from **every** day of the
   series take the error `h` days later (`(k.shift(-h) - k).dropna()`); if
   `widen` is true the bound is `1.96 * sd * sqrt(h)`, otherwise `1.96 * sd`;
   it returns the share of absolute errors within the bound, with three
   decimals.
4. For `h = 1, 10, 40` print the two coverages as `h root constant`, one per
   line.

**Expected output:**

```
2.276
1 162.0 170.9
10 152.3 180.5
40 138.2 194.7
1 0.953 0.953
10 0.925 0.411
40 0.969 0.19
```

With the square root rule the coverage is near 95% at all three horizons. A
constant width is right for one day only; at a 40-day horizon the interval it
calls "95%" holds the truth one time in five. The width of an interval is a
function of the horizon too.
