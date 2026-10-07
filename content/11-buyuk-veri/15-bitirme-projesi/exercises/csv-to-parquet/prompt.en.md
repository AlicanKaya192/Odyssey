Convert a 400 000-row CSV into a single Parquet file in pieces of 100 000
rows.

**What to do:**

1. Read with `pd.read_csv("orders.csv", chunksize=100_000, dtype=NUMERIC)`.
2. Add a `month` column to every piece (the first 7 characters of
   `order_time`).
3. On the first piece open `pq.ParquetWriter("orders.parquet", schema,
   compression="zstd")`, write every piece with `write_table`, close it at
   the end.
4. Print: the number of rows, the number of row groups, the CSV and Parquet
   sizes (MB, one decimal, on one line).
5. Read only the `month` column and print how many different months there
   are.

**Expected output:**

```
400000
4
24.1 7.1
12
```
