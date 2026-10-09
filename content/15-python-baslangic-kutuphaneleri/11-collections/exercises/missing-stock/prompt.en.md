Write the function `missing_stock(order, stock)`: `order` is the list of
ordered products, `stock` the list of products in the warehouse (a product
can occur several times). Return, as a dictionary, how many of each product
are **missing** to fill the order. A `Counter` difference drops the ones
falling below zero by itself.

**Expected output:**

```
{'pen': 2}
```
