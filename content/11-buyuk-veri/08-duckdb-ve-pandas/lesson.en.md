# DuckDB and pandas Together

DuckDB and pandas are not rivals but partners. DuckDB can query a pandas table
directly **by its variable name**, and hands the result back to pandas in one
line. So at every step of an analysis you can choose the tool that suits that
step best: SQL to filter and join big files, pandas for the final shaping and
charts.

In this section we move back and forth between the two worlds, look at the
jobs that are tedious in pandas but easy in SQL (joins, window functions),
and measure which tool is really faster in which situation.

In the examples a million orders sit both in memory (`orders`) and on disk
(`orders.parquet`):

```python
import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(1_000_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)
```

## Querying a table by name

Writing the name of a pandas variable after `FROM` is enough:

```python
print(duckdb.sql("""
    SELECT city, count(*) AS n
    FROM orders
    WHERE quantity >= 4
    GROUP BY city
    ORDER BY n DESC
    LIMIT 3
"""))
```

```text
┌──────────┬───────┐
│   city   │   n   │
│ varchar  │ int64 │
├──────────┼───────┤
│ Istanbul │ 75382 │
│ Ankara   │ 35488 │
│ Izmir    │ 28806 │
└──────────┴───────┘
```

When DuckDB cannot find a table called `orders`, it looks for a variable with
that name in Python; it reads the `DataFrame` it finds as a table. If there is
no such variable either, it raises an error:

```text
CatalogException: Catalog Error: Table with name no_such_frame does not exist!
```

## Joining a file with a table

Let the customer information be in a small pandas table and the orders in a
big Parquet file. Each customer has a segment (`new`, `regular`, `vip`):

```python
ids = pd.RangeIndex(1, 250_000)
customers = pd.DataFrame({
    "customer_id": ids,
    "segment": pd.Series(["new", "regular", "vip"]).iloc[ids % 3].values,
})
```

Let us join the two in a single SQL query:

```python
print(duckdb.sql("""
    SELECT c.segment, count(*) AS orders, round(avg(o.unit_price), 2) AS avg_price
    FROM 'orders.parquet' AS o
    JOIN customers AS c USING (customer_id)
    GROUP BY c.segment
    ORDER BY c.segment
"""))
```

```text
┌─────────┬────────┬───────────┐
│ segment │ orders │ avg_price │
│ varchar │ int64  │  double   │
├─────────┼────────┼───────────┤
│ new     │ 333337 │    737.81 │
│ regular │ 333859 │    735.27 │
│ vip     │ 332804 │    737.53 │
└─────────┴────────┴───────────┘
```

- `AS o`, `AS c`: short aliases for the tables.
- `JOIN ... USING (customer_id)`: join on the column with the same name in
  both tables. A short way of writing the SQL track's
  `ON o.customer_id = c.customer_id`.
- One side is a file on disk, the other a table in memory; to DuckDB it makes
  no difference.

## Window functions and `QUALIFY`

"Each customer's **first** order" takes sorting, grouping and filtering in
pandas. In SQL it is one condition with a window function:

```python
print(duckdb.sql("""
    SELECT customer_id, order_id, order_time
    FROM 'orders.parquet'
    QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1
    ORDER BY customer_id
    LIMIT 3
"""))
```

```text
┌─────────────┬──────────┬─────────────────────┐
│ customer_id │ order_id │     order_time      │
│    int64    │  int64   │      timestamp      │
├─────────────┼──────────┼─────────────────────┤
│           1 │    47287 │ 2024-01-18 06:16:44 │
│           2 │   177677 │ 2024-03-06 01:03:09 │
│           3 │   180262 │ 2024-03-06 23:25:00 │
└─────────────┴──────────┴─────────────────────┘
```

- `row_number() OVER (PARTITION BY customer_id ORDER BY order_time)`: sorts
  each customer's orders by time and numbers them 1, 2, 3 … (the window
  functions from the SQL track).
- `QUALIFY`: filters by the result of a window function. `WHERE` cannot see
  window functions; in SQL Server you wrote a subquery for this, in DuckDB
  `QUALIFY` is enough.

There are 245 461 customers in all, and the query gives exactly one row for
each.

A window also works on top of the result of grouping. Monthly revenue and
the running total up to that month:

```python
print(duckdb.sql("""
    SELECT strftime(order_time, '%Y-%m') AS month,
           round(sum(quantity * unit_price) / 1e6, 1) AS revenue_m,
           round(sum(sum(quantity * unit_price))
                 OVER (ORDER BY strftime(order_time, '%Y-%m')) / 1e6, 1) AS running_m
    FROM 'orders.parquet'
    GROUP BY month
    ORDER BY month
    LIMIT 4
"""))
```

```text
┌─────────┬───────────┬───────────┐
│  month  │ revenue_m │ running_m │
│ varchar │  double   │  double   │
├─────────┼───────────┼───────────┤
│ 2024-01 │     137.9 │     137.9 │
│ 2024-02 │     129.9 │     267.8 │
│ 2024-03 │     138.5 │     406.3 │
│ 2024-04 │     134.0 │     540.4 │
└─────────┴───────────┴───────────┘
```

`sum(sum(...)) OVER (...)`: the inner `sum` is the month's revenue, the outer
`sum ... OVER` the total of the months up to that one.

## A parameterised query

If you need to put a value from outside into a query, do not join strings;
give it with a **question mark**:

```python
def city_orders(city):
    return duckdb.execute(
        "SELECT count(*) FROM 'orders.parquet' WHERE city = ?", [city]
    ).fetchone()[0]

print(city_orders("Izmir"), city_orders("Konya"))
print(city_orders("Izmir' OR '1'='1"))
```

```text
129921 69896
0
```

- `duckdb.execute(query, [values])`: each `?` is replaced by the next value
  in the list.
- The value goes **as data**, not as part of the query. The malicious text on
  the last line could not break the query; since there is no such city, it
  returned 0. Had you joined it in with an f-string, `OR '1'='1'` would become
  part of the query and count every order (tried on this machine: 1 000 000).
  This is the same **SQL injection** attack you saw in the Python and API
  tracks.

## Using one result in another query

If you put the result of `duckdb.sql(...)` in a variable, you can use that
variable as a table in the next query too:

```python
cash = duckdb.sql("SELECT * FROM 'orders.parquet' WHERE payment = 'cash'")
print(duckdb.sql("SELECT count(*), round(avg(unit_price), 2) FROM cash").fetchall())
```

```text
[(80480, 740.75)]
```

`cash` is not a table yet but a **recipe**: the query only runs when it is
used. A comfortable way to split a long analysis into readable steps.

## Let DuckDB summarise, let pandas shape

Let DuckDB do the heavy work and handle the small result with pandas'
convenient tools (`pivot`, ratios, charts):

```python
monthly = duckdb.sql("""
    SELECT strftime(order_time, '%Y-%m') AS month, category,
           sum(quantity * unit_price) AS revenue
    FROM 'orders.parquet'
    GROUP BY month, category
""").df()
table = monthly.pivot(index="month", columns="category", values="revenue")
share = (table.div(table.sum(axis=1), axis=0) * 100).round(1)
print(share.head(3))
```

```text
category  books  clothing  electronics  home  sports  toys
month                                                     
2024-01     5.8      16.8         48.0  12.9    11.0   5.6
2024-02     5.7      16.6         48.7  12.7    10.8   5.5
2024-03     5.7      16.7         48.1  13.0    10.8   5.6
```

DuckDB brought a million rows down to 72 (12 months × 6 categories); pandas
turned them into a month × category table and worked out the shares within
each month. Electronics is nearly half the revenue.

## Which one when? Let us measure

It is easy to assume "DuckDB is always faster". I measured the same jobs on
this computer (the fastest of three tries, a million orders):

| Job | pandas | DuckDB |
|---|---|---|
| Table in memory, city as `str`: revenue per city | 0.044 s | 0.132 s |
| Table in memory, city as `category`: the same job | 0.019 s | 0.003 s |
| Each customer's first order | 0.283 s | 0.514 s |
| Revenue per city from a CSV file (Section 7) | 1.78 s | 0.208 s |

What comes out of this:

1. **If the data is in a file, DuckDB.** It does the reading and the
   calculation together, with only the columns needed and on all cores.
2. **If the data is already in memory with the right types, both are fast.**
   Moving a job pandas does on a table in memory over to DuckDB is not always
   a win.
3. **When giving DuckDB a pandas table, make text `category`.** Reading
   pandas' `str` columns is expensive for DuckDB; with `category` the same
   job went from 0.132 s to 0.003 s. The type choices from Section 2 pay off
   here too.
4. **Turning the result into pandas has a cost.** The first-order query stayed
   slow because it turned a 245 461-row result into a `DataFrame`. If the
   result is big, keep working on it in DuckDB without taking it into pandas,
   or write it straight to a file (`COPY`).

The choice is about **readability** as much as speed: joins and window jobs
are usually shorter and clearer in SQL; step-by-step data cleaning and charts
are more comfortable in pandas.

## Summary

- DuckDB queries a pandas table by its variable name: `FROM orders`.
- A file and a table in memory can be joined in one query
  (`JOIN ... USING (...)`).
- `QUALIFY` filters by the result of a window function: "each customer's
  first order" is a single condition.
- A value from outside is given with `?` (`duckdb.execute(query, [value])`);
  joining strings opens the door to SQL injection.
- You can put a result in a variable and use it as a table in the next query.
- Reading from files DuckDB is very fast; on a table in memory pandas is fast
  too. Make text `category` when giving DuckDB a table, and avoid turning a
  big result into pandas.
