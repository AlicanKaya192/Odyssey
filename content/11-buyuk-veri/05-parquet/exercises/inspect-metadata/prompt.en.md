Get a Parquet file's summary without reading any data.

**What to do:**

1. The starter code writes 200 000 orders as `orders.parquet` in groups of
   50 000 rows.
2. Open the file with `pq.ParquetFile`.
3. Print the number of rows, row groups and columns on one line
   (`metadata.num_rows`, `num_row_groups`, `num_columns`).
4. Print the column names (`schema_arrow.names`) in a loop, each on its own
   line.
5. Print the number of rows in the first row group.

**Expected output:**

```
200000 4 8
order_id
order_time
customer_id
city
category
quantity
unit_price
payment
50000
```
