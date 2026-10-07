The pipeline's first step: estimate the memory of a 200 000-row CSV from a
small sample and compare the estimate with the real value.

**What to do:**

1. `write_orders_csv("orders.csv", 200_000)` is ready. Print the file's size
   on disk in MB (one decimal).
2. Read the first 5000 rows with types (`DTYPES` is ready); multiply the
   memory per row (`memory_usage(deep=True)`) by 200 000 and print it in MB
   (one decimal).
3. Read the whole file with the same types and print the real memory in MB
   (one decimal).
4. Print whether the estimate differs from the real value by less than 2%.

**Expected output:**

```
12.0
9.0
9.0
True
```
