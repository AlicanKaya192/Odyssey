The input of a model that forecasts today's sales cannot contain today's
sales. Compare two features.

**What to do:**

1. Read the file as a series `s` with a date index.
2. Build two features: `naive = s.rolling(7).mean()` and
   `safe = s.shift(1).rolling(7).mean()`.
3. For 9 March 2024 print both, rounded to one decimal, on one line.
4. Check the same two numbers by hand: print the mean of 3–9 March and the
   mean of 2–8 March, rounded to one decimal, on one line.
5. Print how many `NaN` values `safe` has at the start.
6. Build the same feature for a model forecasting 7 days ahead
   (`s.shift(7).rolling(7).mean()`) and print its value for 9 March 2024,
   rounded to one decimal.

**Expected output:**

```
283.7 282.0
283.7 282.0
7
283.1
```

The window of `naive` includes 9 March; `safe` ends on 8 March. If you
forecast seven days ahead, the last value known when you forecast is the one
seven days earlier, and the window has to end there too.
