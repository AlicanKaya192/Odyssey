Imagine you only have monthly totals, and expand them to daily: first
the wrong way, then the right way.

**What to do:**

1. Read `store_sales.csv`; compute the monthly totals of 2024 with
   month-start labels: `s.loc["2024"].resample("MS").sum()`.
2. **The wrong way:** `monthly.resample("D").ffill()`. Print the number of
   rows and the last date (`"%Y-%m-%d"`) on one line.
3. Print the March total of the wrong series.
4. **The right way:** divide each month's total by its number of days
   (`monthly / monthly.index.days_in_month`), build an index of every day of
   2024 (`pd.date_range`) and spread it over the days with
   `reindex(idx, method="ffill")`.
5. Print the March total of the right series, rounded to one decimal.
6. For 9 March 2024 print the spread value (one decimal) and the real sales
   on one line.

**Expected output:**

```
336 2024-12-01
276489
8919.0
287.7 384
```

The wrong way has two mistakes at once: 30 days of December are lost, and
March is swollen 31 times. The right way keeps the monthly total, but look at
the last line: a Saturday gets the month's average. Monthly data has no days
of the week; upsampling does not bring them back.
