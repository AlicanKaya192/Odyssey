The lines you need to move between pandas and DuckDB.

## pandas → DuckDB

```python
duckdb.sql("SELECT ... FROM orders")        # by variable name
con = duckdb.connect()
con.register("t", orders)                   # show it under another name
con.sql("SELECT ... FROM t")
```

Make the text columns of a table you give DuckDB `category`: in this
section's measurement the same query took 0.132 s with `str` and 0.003 s with
`category`.

## DuckDB → pandas

```python
duckdb.sql("SELECT ...").df()               # a DataFrame
duckdb.sql("SELECT ...").fetchall()         # a list of tuples
```

If the result is big, `.df()` is expensive; if you can, summarise in DuckDB
and take the small result.

## Parameters

```python
duckdb.execute("SELECT ... WHERE city = ? AND quantity >= ?", ["Izmir", 3])
```

Every value coming from a user, a file or anywhere outside is given with
`?`; it is not added to the query with an f-string.

## Using a result step by step

```python
cash = duckdb.sql("SELECT * FROM 'orders.parquet' WHERE payment = 'cash'")
duckdb.sql("SELECT city, count(*) FROM cash GROUP BY city")
```

`cash` is a recipe; it runs when used.

## Joins and windows

```sql
SELECT ...
FROM 'orders.parquet' AS o
JOIN customers AS c USING (customer_id);

SELECT *
FROM 'orders.parquet'
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1;
```

## Which one when?

| Situation | Choice |
|---|---|
| The data is in a file, and big | DuckDB |
| Joins, windows, "the first of each group" | DuckDB (SQL is shorter) |
| The data is in memory, with the right types, small to medium | pandas is enough |
| Step-by-step cleaning, charts, `pivot` | pandas |
| Data that does not fit in memory | DuckDB |
