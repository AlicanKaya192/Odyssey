In `orders.csv` the order time is written day first:
`03.01.2024 05:12`. First see the trap with your own eyes, then read the
file correctly.

**What to do:**

1. Convert this small series to dates **without a format** and print the
   month numbers as a list (`.dt.month.tolist()`):

   ```python
   sample = pd.Series(["09.03.2024", "10.03.2024", "11.03.2024"])
   ```

2. Convert the same series with `format="%d.%m.%Y"` and print the month
   numbers.
3. Read `orders.csv`; convert the `ordered_at` column with
   `format="%d.%m.%Y %H:%M"`.
4. Print the first and the last order time on one line.
5. Print the number of orders per month:
   `ordered.dt.month.value_counts().sort_index().to_dict()`.

**Expected output:**

```
[9, 10, 11]
[3, 3, 3]
2024-01-03 05:12:00 2024-04-30 20:47:00
{1: 51, 2: 62, 3: 65, 4: 59}
```

The first line is the trap: all three were in March, but read without a
format they became September, October and November, with no error and no
warning. The last line is a sanity check: the orders run from January to
April, across four months. Had the result spread over twelve months, day and
month would have been swapped.
