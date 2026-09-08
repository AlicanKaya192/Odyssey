Return how many products are in each category.

Columns: `category` and `item_count`. Sort alphabetically by category.

```
category   item_count
---------  ----------
Accessory  6         
Computer   2         
Display    2         
Software   2         
```

Without `GROUP BY`, `COUNT(*)` gives **a single number** for the whole
table (12). If you want one number per category you have to split the rows
into sets first.

The result should be four rows — there are four different categories.
