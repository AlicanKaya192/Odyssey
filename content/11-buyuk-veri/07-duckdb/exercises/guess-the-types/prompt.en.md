Ask DuckDB and pandas for the types of the same CSV.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 50_000)`.
2. With DuckDB, take the `column_name` and `column_type` columns from the
   result of `DESCRIBE SELECT * FROM 'orders.csv'` (`fetchall()`); print the
   column name and type on each line.
3. On the last line print the type pandas chose for the `order_time` column
   of the same file.

**Expected output:**

```
order_id BIGINT
order_time TIMESTAMP
customer_id BIGINT
city VARCHAR
category VARCHAR
quantity BIGINT
unit_price DOUBLE
payment VARCHAR
str
```

DuckDB recognised the date; pandas left it as text.
