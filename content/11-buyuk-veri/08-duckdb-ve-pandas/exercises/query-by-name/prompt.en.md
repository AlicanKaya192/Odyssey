Query a pandas table in memory by its variable name with DuckDB.

**What to do:**

1. Build the table `df = make_orders(100_000)`.
2. Writing `FROM df` inside `duckdb.sql(...)`, find the number of orders per
   payment method; sort by the count, largest first.
3. Get the result with `fetchall()` and print the payment method and the
   count on each line.

**Expected output:**

```
card 72243
transfer 19885
cash 7872
```
