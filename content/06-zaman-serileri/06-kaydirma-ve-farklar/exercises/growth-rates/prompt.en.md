The same question, two different comparisons: against the previous month
and against the same month last year.

**What to do:**

1. Read the file and compute each month's **daily mean**:
   `s.resample("ME").mean()`. (The mean rather than the total, to keep month
   length out of it.)
2. Print the month-on-month percentage change (`pct_change() * 100`) for the
   first four months of 2024 as a list rounded to one decimal.
3. Print the year-on-year percentage change (`pct_change(12) * 100`) for the
   same four months as a list.
4. Print the mean of the year-on-year changes of the twelve months of 2024,
   rounded to one decimal.

**Expected output:**

```
[-11.5, -0.3, -1.7, -7.3]
[11.9, 12.8, 16.4, 10.5]
13.0
```

Someone looking at the first line says "sales are falling"; someone looking
at the second says "we are growing by more than 10% a year". The
month-on-month fall is the seasonality seen every year after the December
peak.
