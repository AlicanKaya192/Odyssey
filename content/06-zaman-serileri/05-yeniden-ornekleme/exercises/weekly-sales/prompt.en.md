Add daily sales up by week, and watch out for partial weeks.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Compute the weekly total (`resample("W").sum()`) and the number of days in
   each week (`resample("W").count()`).
3. Print the first week's total and number of days on one line.
4. Print the total number of weeks and the number of **full** (7-day) weeks
   on one line.
5. Among the full weeks, print the label (`"%Y-%m-%d"`) and total of the week
   with the highest total on one line.
6. Print the same for the full week with the lowest total.

**Expected output:**

```
582 2
158 156
2024-12-29 2717
2022-07-03 1357
```

The first week holds only two days. Had you looked for "the worst week"
without dropping the partial ones, that would have been the answer; in
reality it is the first week of July 2022.
