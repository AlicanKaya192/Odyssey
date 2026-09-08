Return the categories that have **more than two** products.

Columns: `category` and `item_count`. Sort by category.

```
category   item_count
---------  ----------
Accessory  6         
```

The result is one row: of the four categories only one has more than two
products.

**Do not write `WHERE COUNT(*) > 2`** — you will get an error:

```
An aggregate may not appear in the WHERE clause
```

The reason is the processing order: `WHERE` runs **before** the groups
exist, so there is nothing to count. There is a separate piece that
filters groups.
