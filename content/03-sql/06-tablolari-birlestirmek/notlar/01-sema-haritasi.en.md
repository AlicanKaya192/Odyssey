Throughout the intermediate level you will work with the same eight
tables. This note keeps the map on one page; coming back to it while
writing a query is normal.

## The tables

| Table | What it holds | Rows |
|---|---|---|
| `categories` | product categories | 4 |
| `suppliers` | suppliers | 4 |
| `products` | products | 12 |
| `customers` | customers | 6 |
| `employees` | employees | 6 |
| `orders` | orders | 10 |
| `order_items` | order lines | 20 |
| `shipments` | shipping records | 6 |

## The columns

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">categories</span><span class="anat-body"><code>code</code>, <code>name</code></span></div>
    <div class="anat-row"><span class="anat-label">suppliers</span><span class="anat-body"><code>code</code>, <code>name</code>, <code>city</code>, <code>country</code></span></div>
    <div class="anat-row"><span class="anat-label">products</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>category_code</code>, <code>supplier_code</code>, <code>price</code>, <code>stock</code></span></div>
    <div class="anat-row"><span class="anat-label">customers</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>city</code>, <code>country</code>, <code>joined</code></span></div>
    <div class="anat-row"><span class="anat-label">employees</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>title</code>, <code>manager_id</code>, <code>hired</code></span></div>
    <div class="anat-row"><span class="anat-label">orders</span><span class="anat-body"><code>id</code>, <code>customer_id</code>, <code>employee_id</code>, <code>order_date</code>, <code>status</code></span></div>
    <div class="anat-row"><span class="anat-label">order_items</span><span class="anat-body"><code>order_id</code>, <code>product_id</code>, <code>quantity</code>, <code>unit_price</code></span></div>
    <div class="anat-row"><span class="anat-label">shipments</span><span class="anat-body"><code>order_id</code>, <code>shipped_date</code>, <code>carrier</code></span></div>
  </div>
</figure>

## The links

Which column points at which table:

| This column | Links to |
|---|---|
| `products.category_code` | `categories.code` |
| `products.supplier_code` | `suppliers.code` |
| `orders.customer_id` | `customers.id` |
| `orders.employee_id` | `employees.id` |
| `order_items.order_id` | `orders.id` |
| `order_items.product_id` | `products.id` |
| `shipments.order_id` | `orders.id` |
| `employees.manager_id` | `employees.id` (to itself) |

The `_id` and `_code` suffixes are not a coincidence: if a column name
looks like another table's key, it most likely points there. It is the
first thing to look for in an unfamiliar database.

## Links that can be empty

Three links can be `NULL`, and those are the places that need a
`LEFT JOIN`:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">products.supplier_code</span><span class="anat-body">Empty on three products — no supplier recorded.</span></div>
    <div class="anat-row"><span class="anat-label">orders.employee_id</span><span class="anat-body">Empty on two orders — placed online, with no sales rep.</span></div>
    <div class="anat-row"><span class="anat-label">employees.manager_id</span><span class="anat-body">Empty on one person — the one at the top.</span></div>
  </div>
</figure>

On top of that, **not every order has a shipping record**: six of the ten
orders have shipped. `orders` and `shipments` need a `LEFT JOIN` between
them.

## Common joins

```sql
-- product + category name
FROM products p JOIN categories c ON p.category_code = c.code

-- product + supplier (keeping products with no supplier)
FROM products p LEFT JOIN suppliers s ON p.supplier_code = s.code

-- order + customer
FROM orders o JOIN customers c ON o.customer_id = c.id

-- an order's lines + product name
FROM orders o
JOIN order_items i ON o.id = i.order_id
JOIN products p ON i.product_id = p.id

-- order + shipment (keeping unshipped orders)
FROM orders o LEFT JOIN shipments s ON o.id = s.order_id

-- employee + their manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id
```

## The line total

`order_items` does **not** store a total per row; it is calculated:

```sql
i.quantity * i.unit_price
```

`unit_price` is the product's price on that day, while `products.price` is
today's price. The two can differ, and that is deliberate — when a price
changes, the totals of old orders must not change with it.
