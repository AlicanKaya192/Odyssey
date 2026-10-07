Build a permanent DuckDB database, produce a summary table in it and write
it to CSV.

**What to do:**

1. Write the table `make_orders(100_000)` as `orders.parquet`.
2. Connect with `con = duckdb.connect("shop.duckdb")`.
3. Build the `orders` table from the Parquet file with
   `CREATE TABLE ... AS SELECT`.
4. Build the `city_summary` table: `city`, the number of orders (`orders`)
   and the revenue rounded to two decimals (`revenue`, the total of
   `quantity * unit_price`); sorted by city.
5. Write `city_summary` with `COPY ... TO 'city_summary.csv' (HEADER)` and
   close the connection.
6. Connect to the database **again**; print the number of rows in the
   `orders` table and close it.
7. Print the first three lines of `city_summary.csv`.

**Expected output:**

```
100000
city,orders,revenue
Adana,6936,11066810.58
Ankara,15971,25958981.76
```
