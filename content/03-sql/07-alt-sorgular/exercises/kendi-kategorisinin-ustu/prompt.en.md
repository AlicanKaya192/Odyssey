Bring back the products priced above the average of **their own
category**.

Columns: `name`, `category_code`, `price`. Sort by name.

```
name     category_code  price  
-------  -------------  -------
Headset  ACC            890.0  
Laptop   COM            24500.0
...
```

The result should be six rows.

This is not the overall average from the first exercise: each product is
compared with the products in **its own category**. An accessory at 890
can be above its category's average while the same price is far below
average among computers.

For that, the subquery has to link to the outer row — which means giving
each side a different alias.
