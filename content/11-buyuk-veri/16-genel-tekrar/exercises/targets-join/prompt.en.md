Join the orders in the Parquet file with the target table in memory, in
DuckDB.

**What to do:**

1. `orders.parquet` (300 000 orders, with a `month` column) and the pandas
   table `targets` (city, target) are ready.
2. With a single DuckDB query, work out the chosen month's revenue per city,
   join it with `targets` using `JOIN ... USING (city)`, and bring back only
   the cities whose revenue reached the target, from largest revenue to
   smallest.
3. Pass the month to the query with `?`: `duckdb.execute(query, [MONTH])`.
4. Print the city, the revenue (two decimals) and the percentage of the
   target reached (one decimal) on each line.

**Expected output:**

```
Ankara 6635981.63 110.6
Izmir 5146542.94 102.9
Antalya 3559928.0 101.7
Trabzon 2047646.76 102.4
```
