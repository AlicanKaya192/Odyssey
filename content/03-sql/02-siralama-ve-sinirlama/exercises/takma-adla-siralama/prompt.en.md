This exercise brings the three parts of the section together.

Bring back the products that are **in stock** (`stock` above zero), return
`name` under the heading `product` and `price` under `amount`, and sort the
result **by `amount` from largest to smallest**.

```
product  amount 
-------  -------
Laptop   24500.0
Desktop  18900.0
...
```

The result should be six rows.

The real point here: **`ORDER BY` can use the alias.** In the previous
section, trying the same alias inside `WHERE` would have raised an error —
`WHERE` runs early, `ORDER BY` runs late.
