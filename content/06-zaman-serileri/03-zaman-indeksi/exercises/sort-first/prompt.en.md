`sales_messy.csv` holds the same shop's 2024 records, but the rows
arrived in scrambled order. A date range cannot be selected without sorting.

**What to do:**

1. Read the file as a series `messy` with a date index.
2. Print whether the index is in order (`is_monotonic_increasing`).
3. Sort with `sort_index()` and print the same check again.
4. Print the first and the last date as `"%Y-%m-%d"` on one line.
5. Select the week of 4–10 March; print the number of rows and the total on
   one line.

**Expected output:**

```
False
True
2024-01-01 2024-12-31
8 1978
```

Look at the last line: **eight** rows came back for a seven-day week. The
total is right (1978, as in the clean file), but one day is written twice.
The next exercise resolves it.
