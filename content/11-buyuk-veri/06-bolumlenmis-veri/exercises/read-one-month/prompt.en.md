Read only June from data partitioned by month and compare with reading
every folder.

**What to do:**

1. The starter code writes 200 000 orders in the
   `orders/month=YYYY-MM/part-0.parquet` layout.
2. Read only the file `orders/month=2024-06/part-0.parquet`. Print its
   number of rows and its revenue (the total of `quantity * unit_price`, two
   decimals) on one line.
3. Read all the files (`Path("orders").glob("month=*/*.parquet")`) and join
   them; print how many files were read.
4. From the joined table filter those whose `order_time` month is 6; print
   whether the two ways give the same number of rows.

**Expected output:**

```
16392 26273056.88
12
True
```
