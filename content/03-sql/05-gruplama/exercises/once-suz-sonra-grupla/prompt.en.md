This exercise brings the whole section together: two separate filters, a
grouping, and a sort on two criteria.

Count only the products that are **in stock** (`stock` above zero), group
them by category, and return the categories that still have **at least
two** products.

Columns: `category` and `item_count`. Sort by the count descending,
breaking ties by category.

```
category   item_count
---------  ----------
Accessory  5         
Computer   2         
Software   2         
```

Accessory has six products but one is out of stock; because filtering
happens before grouping, the count comes out as five. The Display category
is missing entirely: both of its products are out of stock.

The order is fixed: `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`.

Since `ORDER BY` runs last you can use the alias there — even though you
cannot in `HAVING`.
