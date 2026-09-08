Return how many orders each customer has.

**Customers who have never ordered must also be in the list**, showing `0`
next to them.

Columns: `customer` and `order_count`. Sort by the count descending,
breaking ties by customer name.

```
customer       order_count
-------------  -----------
Nova Retail    3          
Bright Office  2          
Delta Systems  2          
Helix Studio   2          
...
```

The result should be six rows.

There are two traps here at once:

1. Write a plain `JOIN` and the customer with no orders **drops off the
   list**.
2. Write `COUNT(*)` and that customer shows **1** rather than 0 — because
   the join produces a row with empty columns for them, and `COUNT(*)`
   counts rows.

To avoid the second you have to count a column from the right table.
