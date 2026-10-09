Write the function `top_products(items, n)`: open a database in memory,
set `row_factory` to `sqlite3.Row`, build the table `products (name, price)`
and insert the `items` list with `executemany`. Return the **names** of the
first `n` products by price, highest first, as a list; take the name with
`row["name"]`.

**Expected output:**

```
['bag', 'book']
```
