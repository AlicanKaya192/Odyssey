Find each customer's first order with `QUALIFY`.

**What to do:**

1. The starter code writes 100 000 orders as `orders.parquet`.
2. Put the query that picks each customer's first order with
   `QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1`
   into a variable called `first`.
3. On `first`, find and print three things:
   - how many customers there are (`count(*)`),
   - the number of customers whose first order was in January
     (`month(order_time) = 1`),
   - the `customer_id` and `order_id` of the three customers with the
     smallest customer numbers (each on its own line).

**Expected output:**

```
24512
7049
1 20221
2 61138
3 3294
```
