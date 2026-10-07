Split the same data by month and by day; compare the number of files and
the total size.

**What to do:**

1. Build the table with `make_orders(50_000)` and turn `order_time` into a
   date. Add the columns `month` (`%Y-%m`) and `day` (`%Y-%m-%d`).
2. Write it by month as `by_month/month=.../part-0.parquet` and by day as
   `by_day/day=.../part-0.parquet`. Drop both the `month` and `day` columns
   from every file.
3. For the two folders print on one line the folder's name, the number of
   files and the total size in kilobytes (one decimal)
   (`rglob("*.parquet")`, `stat().st_size`).
4. On the last line print the ratio of the day layout's total to the month
   layout's total (two decimals).

**Expected output:**

```
by_month 12 1366.6
by_day 366 3164.8
2.32
```

The same data, the same rows; but in the daily layout every file carries its
own footer and dictionary, so the total grows.
