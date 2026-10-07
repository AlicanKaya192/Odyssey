Read the file of 100 000 orders in chunks of 30 000 rows and count the
chunks.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 100_000)`.
2. Loop over the reader `pd.read_csv(..., chunksize=30_000)`; add each
   chunk's number of rows to a list.
3. Print the list.
4. Print the total number of rows and the number of chunks on one line.

**Expected output:**

```
[30000, 30000, 30000, 10000]
100000 4
```

The last chunk came out short: the file does not divide evenly by the chunk
size.
