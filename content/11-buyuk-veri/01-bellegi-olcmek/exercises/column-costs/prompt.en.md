Find the three columns that take the most memory in a table of 20 000
orders.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 20_000)` and read it
   into `df`.
2. Get the bytes per column with `df.memory_usage(deep=True)`; remove the
   `Index` row.
3. Sort from largest to smallest and print the first three columns in a
   loop: on each line the column's name and its size in **kilobytes**
   (`/ 1024`, one decimal).
4. On the last line print the table's total in kilobytes (one decimal).

**Expected output:**

```
order_time 527.3
city 282.2
category 279.3
1963.5
```

All three of the top columns are text.
