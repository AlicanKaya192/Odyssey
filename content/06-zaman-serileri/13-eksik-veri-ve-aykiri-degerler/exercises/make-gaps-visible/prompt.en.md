`sales_messy.csv` is a shop's sales for 2024 (`date`, `sales`) as they
came out of the system: the rows are scrambled, some days are written in two
parts, some days are not there at all.

**What to do:**

1. Read the file with `parse_dates=["date"]`.
2. Print the number of rows, the number of distinct days and the number of
   `NaN` values in the `sales` column on one line.
3. Print the dates that appear twice as a sorted list in `"%m-%d"` form.
4. Add up the parts of the same day (`groupby("date")["sales"].sum()`), sort,
   and open a row for every day with `asfreq("D")`. Print the length of the
   result and its number of `NaN` values on one line.
5. Print the missing days as a list in `"%m-%d"` form.
6. Print the lengths of the gaps as a list (the
   `(missing != missing.shift()).cumsum()` counter).

**Expected output:**

```
362 358 0
['03-05', '06-18', '09-09', '11-30']
366 8
['02-10', '02-11', '04-23', '07-15', '07-16', '07-17', '10-29', '12-25']
[2, 1, 3, 1, 1]
```

There was not a single `NaN` in the file, yet 8 days were missing. Missing
data cannot be counted without building a regular index. The gaps are 1 to 3
days long: short enough to be filled.
