Turn a CSV into a single Parquet file without ever taking it fully into
memory.

**What to do:**

1. Write the CSV with `write_orders_csv("orders.csv", 300_000)`.
2. Read the CSV in chunks of 100 000 rows (`parse_dates=["order_time"]`).
3. Turn each chunk into a `pyarrow` table with
   `pa.Table.from_pandas(chunk, preserve_index=False)`. On the first chunk
   open the writer with `pq.ParquetWriter("orders.parquet", table.schema)`;
   write every chunk with `write_table`.
4. Close the writer after the loop.
5. Print the file's number of rows and row groups on one line.
6. Print the `quantity` totals in the CSV and in the Parquet on one line.

**Expected output:**

```
300000 3
667058 667058
```

Three chunks, three row groups; the two totals match.
