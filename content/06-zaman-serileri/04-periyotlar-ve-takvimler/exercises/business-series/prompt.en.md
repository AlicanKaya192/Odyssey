`stock_price.csv` holds a stock's closing price. The market is closed at
weekends; **not having** weekend rows in this series is normal.

**What to do:**

1. Read the file with a date index; take the `close` column into a series
   called `close`.
2. Print the frequency pandas infers (`pd.infer_freq`).
3. Print, on one line, the number of `NaN` values created by putting the
   series on the wrong calendar (`asfreq("D")`) and on the right one
   (`asfreq("B")`).
4. Print the number of trading days in March 2024.
5. Print the **month-end close** for the first three months of 2024: group by
   month (`to_period("M")`) and take `last()`; one line per month as
   `month close`.

**Expected output:**

```
B
312 0
21
2024-01 157.19
2024-02 139.47
2024-03 166.33
```

A price is not a total but a point-in-time value. To make it monthly you do
not add it up; you take the month's **last** value. Had you treated weekends
as "missing" and filled them, you would have invented 312 prices that never
existed.
