For orders that were not cancelled, show each category's revenue and its
**percentage share** of the total.

Columns: `category_code`, `revenue`, `share`. `share` as a percentage
with two places (`DECIMAL(5,2)`). Sort by `revenue`, largest first.

```
category_code  revenue   share
-------------  --------  -----
COM            67900.00  68.47
DIS            12800.00  12.91
ACC            12165.00  12.27
SOF            6300.00   6.35
```

The shares add up to 100.

You need three tables: the amount is in `order_items`, the category in
`products`, the cancelled flag in `orders`. There is no need for a
separate query for the total revenue — there is a window that writes the
total of the groups on every row.

Forget the cancelled ones and SOF comes out as `8700.00`, and every share
shifts.
