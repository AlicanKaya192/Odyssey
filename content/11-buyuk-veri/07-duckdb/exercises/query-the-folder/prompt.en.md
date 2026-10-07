Query the folder partitioned by month as a single table with DuckDB.

**What to do:**

1. The starter code writes 200 000 orders in the
   `orders/month=YYYY-MM/part-0.parquet` layout.
2. Find the number of orders across all files with `'orders/*/*.parquet'`
   and print it.
3. With `read_parquet('orders/*/*.parquet', hive_partitioning = true)` choose
   the first quarter of the year (`month <= '2024-03'`); get the number of
   orders per month sorted by month and print the month and count on each
   line.

**Expected output:**

```
200000
2024-01 16921
2024-02 15911
2024-03 16591
```
