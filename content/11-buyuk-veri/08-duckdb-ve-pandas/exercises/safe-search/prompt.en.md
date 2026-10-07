Write a parameterised search function that takes a city and a minimum
quantity.

**What to do:**

1. The starter code writes 100 000 orders as `orders.parquet`.
2. Write the function `count_orders(city, min_quantity)`: it returns the
   number of orders in `city` whose quantity is `min_quantity` or more. Give
   both values with `?`:
   `duckdb.execute(query, [city, min_quantity]).fetchone()[0]`.
3. Print these on separate lines:
   - `count_orders("Izmir", 3)`
   - `count_orders("Bursa", 5)`
   - `count_orders("Izmir' OR '1'='1", 1)`

**Expected output:**

```
4367
994
0
```

The last line is 0: the malicious text could not become part of the query.
