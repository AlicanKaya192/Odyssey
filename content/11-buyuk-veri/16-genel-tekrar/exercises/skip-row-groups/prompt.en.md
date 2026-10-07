Using Parquet statistics, read only the row groups that may contain December
orders.

**What to do:**

1. `orders.parquet` is ready: 400 000 orders, sorted by time, row groups of
   50 000.
2. In every row group, look at the statistics of the `order_time` column
   (`pf.metadata.row_group(i).column(col).statistics`); choose the groups
   whose largest value is not smaller than `"2024-12"`.
3. Read only those groups with `read_row_group` and count the December orders
   (`order_time` starting with `"2024-12"`).
4. Print the number of groups read and the total number of groups on one
   line, then the December count.
5. Print whether it is the same as the December count from the whole file.

**Expected output:**

```
1 8
33784
True
```
