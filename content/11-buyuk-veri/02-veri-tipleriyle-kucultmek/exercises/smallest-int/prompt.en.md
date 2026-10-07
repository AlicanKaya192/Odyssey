Find the smallest safe type for three whole-number columns in a table of
100 000 orders.

**What to do:**

1. Build the table `df` with `make_orders(100_000)`.
2. Loop over the `quantity`, `customer_id` and `order_id` columns.
3. For each column print on one line: the column's name, its smallest value,
   its largest value and the type (`dtype`) of the result of
   `pd.to_numeric(..., downcast="integer")`.

**Expected output:**

```
quantity 1 5 int8
customer_id 1 24999 int16
order_id 1 100000 int32
```

Three columns, three different types: in this table `customer_id` stays
below 25 000, so it fits into `int16`.
