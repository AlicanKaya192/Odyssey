Find the customers who have never placed an order.

One column: `customer`.

```
customer      
--------------
Quiet Partners
```

Of six customers, only one has never ordered.

This is the most useful `LEFT JOIN` pattern and it has two steps: first
bring back every customer, then filter the ones with **no match**.

When there is no match the right table's columns stay empty; you filter on
that.

The same pattern gives you "products never sold" and "orders never
shipped".
