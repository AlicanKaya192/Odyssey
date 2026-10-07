Join the orders on disk with the customer table in memory and find the
revenue per segment.

**What to do:**

1. The starter code writes 200 000 orders as `orders.parquet` and builds the
   `customers` table (`customer_id`, `segment`).
2. In a single DuckDB query join `'orders.parquet'` and `customers` on
   `customer_id`.
3. Find the number of orders and the revenue in millions of lira (the total
   of `quantity * unit_price` / 1e6, two decimals) per segment; sort by
   segment.
4. Print the segment, the number of orders and the revenue on each line.

**Expected output:**

```
new 66603 109.69
regular 67034 109.75
vip 66363 107.99
```
