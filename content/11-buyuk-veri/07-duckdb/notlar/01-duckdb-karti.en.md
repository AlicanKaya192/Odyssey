The lines you will write most often with DuckDB.

## Query and result

```python
import duckdb

r = duckdb.sql("SELECT ... FROM 'orders.parquet'")
print(r)              # a boxed table
r.fetchall()          # [(...), (...)] a list of tuples
r.fetchone()          # the first row, one tuple
r.df()                # a pandas DataFrame
```

## Reading files

```sql
FROM 'orders.parquet'                       -- one file
FROM 'orders.csv'                           -- CSV works too
FROM 'orders/*/*.parquet'                   -- wildcard: every file
FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)
FROM read_csv('zip.csv', types = {'zip': 'VARCHAR'})   -- give a type by hand
```

## Getting to know a table

```sql
DESCRIBE SELECT * FROM 'orders.csv';
SUMMARIZE SELECT * FROM 'orders.parquet';
SELECT column_name, column_type FROM (DESCRIBE SELECT * FROM 'orders.csv');
```

## A permanent database

```python
con = duckdb.connect("shop.duckdb")
con.sql("CREATE TABLE orders AS SELECT * FROM 'orders.parquet'")
con.sql("SELECT count(*) FROM orders")
con.close()
```

## Writing to a file

```sql
COPY (SELECT ...) TO 'out.csv' (HEADER);
COPY (SELECT ...) TO 'out.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY (SELECT ...) TO 'out' (FORMAT parquet, PARTITION_BY (month));
```

`PARTITION_BY` creates the partition folders itself: `out/month=2024-01/data_0.parquet`.

## Useful functions

| Function | What it does |
|---|---|
| `count(*)`, `sum`, `avg`, `min`, `max` | The aggregate functions you know |
| `count(DISTINCT x)` | The exact number of different values |
| `approx_count_distinct(x)` | The approximate number of different values (little memory) |
| `strftime(t, '%Y-%m')` | Turns a date into text |
| `round(x, 2)` | Rounds |
| `x::DOUBLE`, `x::VARCHAR` | Converts a type |
| <code>a &#124;&#124; b</code> | Joins strings |

## This track's measurement (a million orders, revenue per city)

| Way | Time |
|---|---|
| pandas, CSV | 1.78 s |
| DuckDB, CSV | 0.208 s |
| pandas, Parquet | 0.059 s |
| DuckDB, Parquet | 0.011 s |
