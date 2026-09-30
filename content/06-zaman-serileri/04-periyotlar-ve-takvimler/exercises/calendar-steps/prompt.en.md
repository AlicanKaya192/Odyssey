Four subscriptions started on different days of the month. For each,
the "renewal day one month later" is needed. This exercise has no file.

```python
starts = ["2024-01-31", "2024-02-29", "2024-03-31", "2024-08-30"]
```

**What to do:**

1. For each start compute two dates: **30 days later**
   (`pd.Timedelta(days=30)`) and **one month later**
   (`pd.DateOffset(months=1)`). Print the three as `start 30days 1month`
   (`"%Y-%m-%d"`) on one line.
2. For 9 March 2024 print the last day of its month (`MonthEnd(0)`).
3. Print how many days are left from 9 March 2024 until the month end.

**Expected output:**

```
2024-01-31 2024-03-01 2024-02-29
2024-02-29 2024-03-30 2024-03-29
2024-03-31 2024-04-30 2024-04-30
2024-08-30 2024-09-29 2024-09-30
2024-03-31
22
```

In the first line the two methods are one day apart: 30 days later spills
into March, one month later lands on February's last day. In the third line
they fall on the same day, which is exactly why the mistake goes unnoticed
for so long.
