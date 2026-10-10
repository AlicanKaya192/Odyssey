`unmatched_orders(orders, customers)` should return the numbers (an `int`
list) of the orders that have **no** match in the customer table. Merge with
`how="outer"` and `indicator=True`; pick those whose `_merge` column is
`"left_only"`. **Do not write a loop.**

**Expected output:**

```
[4]
```
