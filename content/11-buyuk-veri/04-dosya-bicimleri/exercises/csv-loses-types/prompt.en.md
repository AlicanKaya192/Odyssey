Write a table with its types set to CSV and to Parquet, read them back and
see which one keeps the types.

**What to do:**

1. The starter code prepares `df` with 20 000 orders (date and categories
   set).
2. Write `df` as `orders.csv` (`index=False`) and as `orders.parquet`.
3. Read both back.
4. For each, print on one line the format's name (`csv` / `parquet`) and the
   types of the `order_time` and `city` columns.

**Expected output:**

```
csv str str
parquet datetime64[us] category
```
