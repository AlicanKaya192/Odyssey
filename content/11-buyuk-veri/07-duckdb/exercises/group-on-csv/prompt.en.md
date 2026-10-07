Without taking a CSV file into memory, find the number of orders and the
mean price per category with DuckDB.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 200_000)`.
2. With DuckDB on `'orders.csv'`: `category`, the number of orders and the
   mean `unit_price` rounded to two decimals; by number of orders, largest
   first.
3. Get the result with `fetchall()` and print each row with its three values
   side by side.

**Expected output:**

```
clothing 44401 551.89
books 43837 191.58
home 39756 477.68
electronics 28040 2557.45
toys 24143 340.94
sports 19823 808.52
```
