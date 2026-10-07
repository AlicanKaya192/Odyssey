Shrink the orders table with types and prove that no value was damaged.

**What to do:**

1. `orders` (200 000 rows) is ready, read with the default types. Print its
   memory in MB (one decimal).
2. Build a copy called `small`: shrink the `order_id`, `customer_id` and
   `quantity` columns with `pd.to_numeric(..., downcast="integer")`; make the
   `city`, `category` and `payment` columns `category`.
3. Print the memory of `small` in MB (one decimal).
4. Print the new types of the `quantity` and `customer_id` columns on one
   line.
5. Print whether the revenue totals (`quantity * unit_price`) of the two
   tables are exactly the same.

**Expected output:**

```
19.2
9.0
int8 int32
True
```
