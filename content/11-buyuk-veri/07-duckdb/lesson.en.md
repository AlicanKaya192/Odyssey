# DuckDB: SQL on Files

In the SQL track you sent queries to a **server**: SQL Server runs as a
separate program and keeps the data inside itself. This section's tool,
DuckDB, is a completely different idea: a database that **runs inside your
Python program**. There is no server to install and no address to connect to;
`import duckdb` is enough. What is more, you do not have to import the data
first: you can write SQL **directly** on CSV and Parquet files.

<figure class="fig">
  <div class="versus">
    <div><h4>SQL Server</h4><p>A separate program, a separate install<br>You import the data into it first<br>Python connects to it at an address<br>Many users, many transactions</p></div>
    <div class="ok"><h4>DuckDB</h4><p>Inside Python, <code>import duckdb</code><br>Queries CSV and Parquet directly<br>No server, no address<br>For analysis: column by column, all cores</p></div>
  </div>
  <figcaption>Both speak SQL, but they were built for different jobs. DuckDB is also called "SQLite for analytics".</figcaption>
</figure>

DuckDB was designed for analysis: it processes data column by column, uses
all of the computer's cores and can work without taking the whole table into
memory. That is why on big files it is often much faster than pandas.

The examples work with three copies of the same million orders:
`orders.csv`, `orders.parquet` and the `orders/` folder partitioned by month.

## The first query

```python
import duckdb

r = duckdb.sql("SELECT count(*) AS orders FROM 'orders.parquet'")
print(r)
print(r.fetchall())
```

```text
┌─────────┐
│ orders  │
│  int64  │
├─────────┤
│ 1000000 │
└─────────┘

[(1000000,)]
```

- `duckdb.sql(...)` runs the query and returns a **result object**; printing
  it draws a boxed table. Under each column its type is written (`int64`).
- `fetchall()` gives the result as a Python list: each row a tuple.
- `FROM 'orders.parquet'`: **a file name in single quotes** stands in for a
  table name. DuckDB works out the format from the extension; `'orders.csv'`
  works the same way.

## Grouping

Everything you learned on the SQL track applies here too:

```python
print(duckdb.sql("""
    SELECT city, count(*) AS orders,
           round(sum(quantity * unit_price) / 1e6, 2) AS revenue_m
    FROM 'orders.parquet'
    GROUP BY city
    ORDER BY revenue_m DESC
    LIMIT 3
"""))
```

```text
┌──────────┬────────┬───────────┐
│   city   │ orders │ revenue_m │
│ varchar  │ int64  │  double   │
├──────────┼────────┼───────────┤
│ Istanbul │ 340437 │     557.0 │
│ Ankara   │ 159984 │    260.83 │
│ Izmir    │ 129921 │     212.5 │
└──────────┴────────┴───────────┘
```

In Section 3 we found this result by reading in chunks and combining with
`groupby` (Istanbul 557.00 million). DuckDB does the same job with a single
query; it thinks about the chunking itself.

`LIMIT 3` is the counterpart of SQL Server's `TOP 3`.

## Taking the result into pandas

If the result of the query is small and you want to carry on with pandas,
`.df()`:

```python
t = duckdb.sql("""
    SELECT city, count(*) AS orders
    FROM 'orders.parquet'
    GROUP BY city
    ORDER BY orders DESC
""").df()
print(type(t).__name__)
print(t.head(3))
```

```text
DataFrame
       city  orders
0  Istanbul  340437
1    Ankara  159984
2     Izmir  129921
```

This is a very handy division of labour for big data: **let DuckDB filter and
summarise the bulk, and hand the small result to pandas.** A million rows came
down to eight; pandas' job is easy now.

## Getting to know a table: `DESCRIBE`

To see a file's columns and types:

```python
print(duckdb.sql("""
    SELECT column_name, column_type
    FROM (DESCRIBE SELECT * FROM 'orders.csv')
"""))
```

```text
┌─────────────┬─────────────┐
│ column_name │ column_type │
│   varchar   │   varchar   │
├─────────────┼─────────────┤
│ order_id    │ BIGINT      │
│ order_time  │ TIMESTAMP   │
│ customer_id │ BIGINT      │
│ city        │ VARCHAR     │
│ category    │ VARCHAR     │
│ quantity    │ BIGINT      │
│ unit_price  │ DOUBLE      │
│ payment     │ VARCHAR     │
└─────────────┴─────────────┘
```

Note: this is a **CSV** file, and DuckDB worked out by itself that the
`order_time` column is a date-time (`TIMESTAMP`). pandas read the same CSV as
`str`; DuckDB looks at the first rows and guesses the types.

## A quick summary: `SUMMARIZE`

`SUMMARIZE` produces, in one go, information such as the smallest, largest
and mean value and the number of different values for each column. The
result is very wide, so we pick a few of its columns:

```python
print(duckdb.sql("""
    SELECT column_name, min, max, approx_unique, round(avg::DOUBLE, 2) AS avg
    FROM (SUMMARIZE SELECT quantity, unit_price, city FROM 'orders.csv')
"""))
```

```text
┌─────────────┬─────────┬──────────┬───────────────┬────────┐
│ column_name │   min   │   max    │ approx_unique │  avg   │
│   varchar   │ varchar │ varchar  │     int64     │ double │
├─────────────┼─────────┼──────────┼───────────────┼────────┤
│ quantity    │ 1       │ 5        │             5 │   2.22 │
│ unit_price  │ 33.69   │ 16646.99 │        216700 │ 736.87 │
│ city        │ Adana   │ Trabzon  │             7 │   NULL │
└─────────────┴─────────┴──────────┴───────────────┴────────┘
```

Notice something: `approx_unique` says **7** for the city, but there are 8
cities. The "approx" in its name means approximate: instead of counting the
different values one by one, DuckDB **estimates** them with very little
memory. With big data such approximate calculations are used on purpose; we
will see how they work in Section 9. If you need the exact number,
`count(DISTINCT city)`.

`avg::DOUBLE`: `::` turns a value into another type. `SUMMARIZE` gives the
mean as text; we turn it into a number first so we can round it.

## Folders and wildcards

With partitioned data there is no need to go through every file one by one.
With `*` (a wildcard) in the file name, DuckDB reads every matching file as a
single table:

```python
print(duckdb.sql("SELECT count(*) FROM 'orders/*/*.parquet'").fetchone())
```

```text
(1000000,)
```

`hive_partitioning = true` brings back the `month=...` information from the
folder names as a column and does the partition pruning by itself:

```python
print(duckdb.sql("""
    SELECT month, count(*) AS orders
    FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)
    WHERE month >= '2024-11'
    GROUP BY month
    ORDER BY month
"""))
```

```text
┌─────────┬────────┐
│  month  │ orders │
│ varchar │ int64  │
├─────────┼────────┤
│ 2024-11 │  82115 │
│ 2024-12 │  85002 │
└─────────┴────────┘
```

The work we did by hand in the last section (`glob`, the month from the
folder name, filtering) was done by a single query; the ten folders other
than November and December were not read.

## Why so fast?

I worked out the revenue per city in four ways (on this computer, the
fastest of three tries):

| Way | Time |
|---|---|
| pandas, CSV | 1.78 s |
| pandas, Parquet (3 columns) | 0.059 s |
| DuckDB, CSV | 0.208 s |
| DuckDB, Parquet | 0.011 s |

DuckDB processed the same CSV eight times faster than pandas. The reasons:

1. **Only the columns needed.** The query wants `city`, `quantity` and
   `unit_price`; DuckDB never parses the other five columns. In Parquet it
   does not even touch them.
2. **All the cores.** pandas usually does a calculation on one core; DuckDB
   splits the work across the cores.
3. **Streaming.** DuckDB reads and processes the file in small batches; it
   does not need the whole table in memory. When grouping, memory holds only
   the groups' intermediate results.

The third point matters most for big data: it is why DuckDB can query files
bigger than its memory. If intermediate results do not fit in memory (a big
sort or join, for example), it carries on by writing them to temporary files.

## A permanent database

`duckdb.sql(...)` uses a temporary database in memory each time. If you want
to keep tables, connect to a file:

```python
con = duckdb.connect("shop.duckdb")
con.sql("CREATE TABLE orders AS SELECT * FROM 'orders.parquet'")
print(con.sql("SELECT count(*) FROM orders").fetchone())
con.close()
```

- `duckdb.connect("shop.duckdb")`: creates the file if it does not exist,
  connects if it does.
- `CREATE TABLE ... AS SELECT ...`: keeps the query's result as a new table.
- `con.close()`: closes the connection. When the program is opened again and
  connects to the same file, the `orders` table is still there.

The `shop.duckdb` file took 10.8 MB with a million orders; DuckDB also stores
its data column by column and compressed.

## Writing the result to a file: `COPY`

`COPY (query) TO 'file'` writes a query's result straight to disk:

```python
duckdb.sql("""
    COPY (SELECT city, count(*) AS orders FROM 'orders.parquet'
          GROUP BY city ORDER BY city)
    TO 'city_counts.csv' (HEADER)
""")
```

The same way you can turn a CSV into Parquet with a single command:

```python
duckdb.sql("""
    COPY (SELECT * FROM 'orders.csv')
    TO 'from_csv.parquet' (FORMAT parquet, COMPRESSION zstd)
""")
```

The resulting file is 11.9 MB and the date column was stored as `TIMESTAMP`:
DuckDB guessed the types; you never gave them.

## Error messages

If you write a column that does not exist, DuckDB says so before running the
query:

```text
BinderException: Binder Error: Referenced column "nosuch" not found in FROM clause!
```

The "binder" is the stage that binds the names in the query to tables; this
error almost always means a typo or the wrong file.

## Differences from SQL Server

T-SQL from the SQL track and DuckDB's SQL are largely the same. Differences
you will meet often:

| SQL Server (T-SQL) | DuckDB |
|---|---|
| `SELECT TOP 3 ...` | `... LIMIT 3` |
| `FORMAT(date, 'yyyy-MM')` | `strftime(date, '%Y-%m')` |
| A table lives in a database | `FROM 'file.parquet'` works too |
| `[column name]` | `"column name"` |

## Summary

- DuckDB is a serverless analysis database that runs inside Python.
- `duckdb.sql("... FROM 'orders.parquet'")`: a file name stands in for a
  table; CSV works too.
- `.fetchall()` gives a Python list, `.df()` a pandas table. Give the bulk of
  the work to DuckDB and the small result to pandas.
- `DESCRIBE` shows the columns and types, `SUMMARIZE` quick statistics; DuckDB
  also guesses the types in a CSV.
- `'folder/*/*.parquet'` reads many files as one table;
  `hive_partitioning = true` brings back the partition column and does the
  pruning.
- It is fast because it processes only the columns needed, on all cores, in
  a stream: eight times faster than pandas on CSV in this measurement.
- `duckdb.connect("file.duckdb")` is a permanent database; `COPY ... TO`
  writes a result to a file.
