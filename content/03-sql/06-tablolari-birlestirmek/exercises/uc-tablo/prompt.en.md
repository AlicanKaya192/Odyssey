Show the lines of order **1005**: the order number, the customer name,
the product name and the quantity.

Columns: `order_id`, `customer`, `product`, `quantity`. Sort by product
name.

```
order_id  customer      product  quantity
--------  ------------  -------  --------
1005      Helix Studio  Desktop  1       
...
```

The result should be three rows — that order has three lines.

You need four tables at once:

- `orders` — the order itself
- `customers` — the customer's name
- `order_items` — the order's lines
- `products` — the product's name

Each `JOIN` is added to the result of the previous one. The links are
`orders.customer_id = customers.id`, `orders.id = order_items.order_id`,
`order_items.product_id = products.id`.

Notice that the customer name repeats on every row: the join multiplies
the order's details across its lines.
