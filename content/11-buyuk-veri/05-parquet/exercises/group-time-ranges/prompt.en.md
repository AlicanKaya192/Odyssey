Read from the statistics which dates each row group covers.

**What to do:**

1. The starter code writes 200 000 orders in groups of 40 000 rows.
2. Find the position of the `order_time` column with
   `schema_arrow.names.index(...)`.
3. For each row group print on one line the group's number and the **date**
   (`.date()`) of the smallest and largest value of the `order_time`
   statistics.

**Expected output:**

```
0 2024-01-01 2024-03-14
1 2024-03-14 2024-05-26
2 2024-05-26 2024-08-07
3 2024-08-07 2024-10-20
4 2024-10-20 2024-12-31
```

The groups split the year into five without overlapping; when filtering by
time, each can be skipped on its own.
