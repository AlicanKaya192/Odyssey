Ask a Parquet file three questions with DuckDB.

**What to do:**

1. Write the table `make_orders(100_000)` as `orders.parquet`
   (`index=False`).
2. With a single `duckdb.sql(...)` query get these three and read them with
   `fetchone()`:
   - the number of orders (`count(*)`),
   - the number of different cities (`count(DISTINCT city)`),
   - the total quantity sold (`sum(quantity)`).
3. Print the three values on separate lines.

**Expected output:**

```
100000
8
222191
```
