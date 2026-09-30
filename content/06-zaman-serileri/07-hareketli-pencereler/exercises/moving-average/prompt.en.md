Smooth daily sales with a 7-day moving average.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Compute the 7-day moving average: `s.rolling(7).mean()`.
3. Print the number of `NaN` values at the start.
4. For 10 March 2024 (a Sunday) print the moving average and the mean of the
   week of 4–10 March, rounded to one decimal, on one line.
5. Print the standard deviation of the raw series and of the moving average,
   rounded to one decimal, on one line.
6. For 9 March 2024 print the exponentially weighted mean
   (`s.ewm(span=7).mean()`) and the moving average, rounded to one decimal,
   on one line.

**Expected output:**

```
6
282.6 282.6
58.9 39.1
299.2 283.7
```

In step four the two numbers are the same: the 7-day mean on a Sunday is the
mean of the week ending that day. In the last line `ewm` is higher, because
it gives the newest day (a high-selling Saturday) more weight.
