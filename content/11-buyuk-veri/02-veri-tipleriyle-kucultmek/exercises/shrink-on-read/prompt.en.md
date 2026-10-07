Read the same file twice: once leaving the types to pandas, once giving the
types yourself. Compare the memory.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 200_000)`.
2. `plain = pd.read_csv("orders.csv")`.
3. Read the table `typed` with `read_csv` using these types:
   - `order_id`, `customer_id`: `"int32"`
   - `quantity`: `"int8"`
   - `unit_price`: `"float32"`
   - `city`, `category`, `payment`: `"category"`
   - `order_time`: a date, with `parse_dates`
4. Print the memory of both tables in MB, rounded to one decimal, on one
   line.
5. Print the shrink ratio (`plain / typed`), rounded to one decimal.
6. Print the types of the `order_time` and `city` columns in `typed` on one
   line.

**Expected output:**

```
19.2 4.6
4.2
datetime64[us] category
```
