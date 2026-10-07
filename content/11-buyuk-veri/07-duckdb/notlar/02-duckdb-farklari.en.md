Things to watch out for in DuckDB if you come from the SQL track. All were
tried on this machine.

## 1. Division gives decimals

```sql
SELECT 5 / 2, 5 // 2;      -- 2.5, 2
```

In SQL Server dividing two whole numbers gives a whole number (`5 / 2 = 2`);
in DuckDB `/` gives a decimal result. For whole-number division, `//`.

## 2. No `TOP`, there is `LIMIT`

```sql
SELECT * FROM 'orders.parquet' ORDER BY unit_price DESC LIMIT 5;
```

## 3. Date functions differ

`strftime(date, '%Y-%m')` instead of `FORMAT(date, 'yyyy-MM')`; the format
letters are the same as Python's.

## 4. Column names are case-insensitive

`SELECT City FROM ...` works even though the column is called `city`.

## 5. CSV types are guessed

DuckDB looks at the first rows of a CSV and chooses the types; it makes the
date a `TIMESTAMP`. It kept a postcode with a leading zero (`01234`) as text.
pandas, on the other hand, turned the same column into a number and made it
`1234`. If the guess is wrong, give the type by hand:

```sql
SELECT * FROM read_csv('zip.csv', types = {'zip': 'VARCHAR'});
```

## 6. Things starting with `approx_` are approximate

`approx_count_distinct(city)` said 7 for 8 cities, and so did `approx_unique`
in `SUMMARIZE`. For the exact number, `count(DISTINCT city)`. Approximate
counting exists because it works with very little memory on very big data
(Section 9).

## 7. Temporary and permanent

`duckdb.sql(...)` uses a temporary database in memory; a table you build
with `CREATE TABLE` is gone when the program closes. To keep it,
`duckdb.connect("file.duckdb")`.

## 8. String concatenation is `||`

`'a' || 'b'` → `'ab'`. Joining strings with `+`, as in SQL Server, does not
exist in DuckDB.
