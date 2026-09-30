`stores.csv` holds the 2024 daily sales of four shops in the long shape:
`date`, `store`, `sales`. Turn it into the wide shape and see what is
missing.

**What to do:**

1. Read the file with `parse_dates=["date"]`.
2. Print each shop's number of rows as a dict:
   `long.groupby("store").size().to_dict()`.
3. Turn it into the wide shape:
   `long.pivot(index="date", columns="store", values="sales")`. Print its
   `shape`.
4. Print the number of `NaN` values in each column as a dict.
5. Print shop D's first valid date as `"%Y-%m-%d"` (`first_valid_index()`).

**Expected output:**

```
{'A': 366, 'B': 366, 'C': 314, 'D': 245}
(366, 4)
{'A': 0, 'B': 0, 'C': 52, 'D': 121}
2024-05-01
```

The long table had 1291 rows; the wide table has 1464 cells. The other 173
cells are days with no row at all in the long table: C's Sundays and D's four
months before it opened.
