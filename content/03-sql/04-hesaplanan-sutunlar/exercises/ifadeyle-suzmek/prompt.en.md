Bring back the products whose stock value (price times stock) is **above
50000**.

Columns: `name`, `price`, `stock`, `stock_value`. Sort by stock value,
largest first.

```
name          price    stock  stock_value
------------  -------  -----  -----------
Office Suite  2400.0   99     237600.0   
Laptop        24500.0  5      122500.0   
...
```

The result should be three rows.

The point here: you cannot use the **alias** inside `WHERE`, but you can
use **the expression itself**. So you will write the calculation twice —
once in `SELECT` where you name it, once in `WHERE` where you filter.

In `ORDER BY` the alias is enough; that runs last.
