Turn the seasonal naive forecast into a quantile forecast and measure it
with the pinball loss.

In the starter code `past` (the errors of 2023), `base` (the seasonal naive
forecast for 2024) and `actual` (the actual values of 2024) are ready.

**What to do:**

1. Write the function `pinball(actual, forecast, q)`:
   `diff = actual - forecast`; the result is the mean of
   `np.maximum(q * diff, (q - 1) * diff)`.
2. For `q = 0.5, 0.8, 0.9, 0.95`:
   - the share to add: `past.quantile(q)`
   - the quantile forecast: `base + share`
   - the pinball loss of that forecast
   - the share of days on which the actual value stayed **at or below** the
     forecast

   For each `q` print a line as `q share loss rate` (the share with one, the
   loss with two and the rate with three decimals).
3. For comparison: print the pinball loss of **the point forecast** (`base`)
   at `q = 0.9` with two decimals.

**Expected output:**

```
0.5 2.0 6.92 0.514
0.8 16.0 4.68 0.801
0.9 23.0 2.84 0.913
0.95 28.0 1.68 0.962
7.3
```

The last column is very close to the stated quantile: the 0.9 quantile stayed
above the truth on 91% of the days. The last line shows the price of using the
point forecast as the 90% limit: two and a half times the pinball loss. The
same forecast, a different question; a different question needs a different
number.
