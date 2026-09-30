Add daily sales up into months.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Assign each day to its month and add up:
   `s.groupby(s.index.to_period("M")).sum()`.
3. Print how many months there are.
4. Print the total of March 2024.
5. Print the month with the highest total and its total on one line
   (`idxmax()`).

**Expected output:**

```
36
8919
2024-12 11335
```

Three years shrank to 36 months. The index is now months rather than days: a
`PeriodIndex`.
