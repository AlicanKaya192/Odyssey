The `products` table also has a `supplier_code` column, and **for some
products it is empty.**

Bring back the `name` and `category` of the products where that column is
empty, in alphabetical order.

```
name          category 
------------  ---------
Headset       Accessory
Office Suite  Software 
Projector     Display  
```

**Careful:** write `WHERE supplier_code = NULL` and you get no rows and no
error. `NULL` is not a value but the absence of one; it cannot be
compared.

Press the **Tables** button if you want to see the table; the empty cells
show up there as `NULL`.
