Read `store_sales.csv` as a series with a date index and try selecting
by date.

**What to do:**

1. Read the file with `index_col="date"` and `parse_dates=True`; take the
   `sales` column into a series called `s`.
2. Print the name of the index's type: `type(s.index).__name__`.
3. Print the sales of 9 March 2024.
4. Print the total sales of March 2024.
5. Print the mean sales of the year 2024, rounded to one decimal.

**Expected output:**

```
DatetimeIndex
384
8919
294.0
```

In the last section you found the March total by writing two conditions.
With the date in the index, writing `"2024-03"` is enough.
