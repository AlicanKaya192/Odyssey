Select ranges from a series with a date index.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Select the week of 4–10 March 2024; print the number of rows and the total
   on one line.
3. Select the first quarter of 2024 (`"2024-01":"2024-03"`); print the number
   of days and the total on one line.
4. Print the mean sales of December 2024, rounded to one decimal.
5. Find the day of 2024 with the highest sales (`idxmax()`); print the date
   as `"%Y-%m-%d"` and that day's sales on one line.

**Expected output:**

```
7 1978
91 26513
365.6
2024-12-28 503
```

The week came back with seven days: a date slice takes the last day too. The
first quarter is 91 days, because 2024 is a leap year and February has 29.
