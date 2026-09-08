# Joining Tables

At the beginner level you worked with a single table. That is not how a
real database looks: the data is split into **pieces** that are linked to
one another.

From this section on you will work with an eight-table order database. The
first job is learning how to bring those tables together.

## Why not keep everything in one table?

We could have stored the supplier's name, city and country in the product
table. Three problems appear:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Repetition</span><span class="anat-body">If the same supplier appears on three products, its name is written three times.</span></div>
    <div class="anat-row"><span class="anat-label">Inconsistency</span><span class="anat-body">When the supplier moves you have to update all three rows; forget one and the data contradicts itself.</span></div>
    <div class="anat-row"><span class="anat-label">Loss</span><span class="anat-body">A supplier with no products yet cannot be recorded anywhere.</span></div>
  </div>
</figure>

The answer is to put each thing in its own table and create a **link**
between them:

```
suppliers.code  <---  products.supplier_code
```

The `products.supplier_code` column is called a **foreign key**: it points
at a row in another table.

The price of this separation is that answering a question now takes two
tables at once. `JOIN` is what does that.

## INNER JOIN

```sql
SELECT p.name, s.name
FROM products p
JOIN suppliers s ON p.supplier_code = s.code;
```

There are three parts:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">FROM products p</span><span class="anat-body">The left-hand table and the short name given to it (an <b>alias</b>).</span></div>
    <div class="anat-row"><span class="anat-label">JOIN suppliers s</span><span class="anat-body">The table being added.</span></div>
    <div class="anat-row"><span class="anat-label">ON ... = ...</span><span class="anat-body"><b>Under what condition</b> two rows match. Without this the join is meaningless.</span></div>
  </div>
</figure>

`INNER JOIN` returns only the **matching** rows. There are twelve products
but three have no supplier recorded, so this query returns **nine** rows.

Three products quietly disappear. No error, no warning.

### Aliases

`p` and `s` are not required, but they are written almost always: the
query gets shorter and you can see which column comes from which table.

There is one case where they are required: **when both tables have a
column with the same name.**

```sql
SELECT name FROM products p JOIN categories c ON p.category_code = c.code;
-- error: Ambiguous column name 'name'
```

Both tables have a `name` column and the server cannot tell which you
meant. You have to write `p.name` or `c.name`.

## LEFT JOIN

If you want those three missing products too:

```sql
SELECT p.name, s.name AS supplier
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code;
```

The result is **twelve** rows. In the three rows with no match, the right
table's columns come back as `NULL`.

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>INNER JOIN</h4>
      <p>Only the <b>matches</b>. You can lose rows from the left table.</p>
    </div>
    <div class="ok">
      <h4>LEFT JOIN</h4>
      <p><b>Every row on the left</b> is kept; with no match the right side comes back empty.</p>
    </div>
  </div>
  <figcaption>"Left" and "right" mean the two sides of FROM and JOIN. There is a RIGHT JOIN too, but it is rarely used: swapping the tables and writing LEFT reads better.</figcaption>
</figure>

### Finding what does not match

This is the most useful thing `LEFT JOIN` does:

```sql
SELECT p.name
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code
WHERE s.code IS NULL;
```

"Products with no supplier recorded" — three rows. The same pattern gives
you "customers with no orders" and "products never sold".

## The trap: a WHERE that kills the LEFT JOIN

This is the most common mistake in the whole topic.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Kills the LEFT JOIN</h4>
      <pre><code>FROM products p
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
WHERE s.country = 'Turkey'</code></pre>
    </div>
    <div class="ok">
      <h4>Keeps the left side</h4>
      <pre><code>FROM products p
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
 AND s.country = 'Turkey'</code></pre>
    </div>
  </div>
  <figcaption>The left one returns 9 rows, the right one 12. The reason: WHERE runs after the join, and rows whose right side is NULL cannot satisfy the condition — the LEFT JOIN quietly becomes an INNER JOIN.</figcaption>
</figure>

The rule: **if you are putting a condition on the right table, write it
inside `ON`**, not inside `WHERE`. `WHERE` runs after the join is done.

The one exception is `IS NULL`: to find the non-matching rows you write it
in `WHERE` on purpose.

## Joining several tables

`JOIN` clauses are written one after another:

```sql
SELECT o.id, c.name AS customer, p.name AS product, i.quantity
FROM orders o
JOIN customers c   ON o.customer_id = c.id
JOIN order_items i ON o.id = i.order_id
JOIN products p    ON i.product_id = p.id;
```

Each `JOIN` is added to the result of the previous one. The order affects
readability but not the result — the server picks the most efficient order
itself.

## Rows multiply

This is what surprises people most while learning `JOIN`.

The `orders` table has **10** orders. Join it with `order_items` and the
result is **20** rows: each order has several lines, and the order's
details repeat for every line.

Think of it this way: a join produces a new table, and that table's row
count can differ from both of the originals.

**The concrete consequence:** after a join, `COUNT(*)` no longer gives the
number of orders but the number of lines. To count orders you need
`COUNT(DISTINCT o.id)`.

## Joining a table to itself

A table can be joined to itself. In the employees table, each record's
manager is in the same table:

```sql
SELECT e.name, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

The same table gets two different aliases and the server treats them as
two separate tables. `LEFT JOIN` is used because the person at the top has
no manager — their `manager` comes back empty.

## JOIN and grouping together

```sql
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
```

There is one more trap here:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(o.id)</span><span class="anat-body"><b>0</b> for a customer with no orders. This is the correct one.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body"><b>1</b> for the same customer, because <code>LEFT JOIN</code> produces one row with empty columns for them and <code>COUNT(*)</code> counts rows.</span></div>
  </div>
  <figcaption>Measured: Quiet Partners has no orders at all. COUNT(*) says 1 and COUNT(o.id) says 0.</figcaption>
</figure>

The rule: **after a `LEFT JOIN`, count a column from the right table**,
not `*`.

## Summary

- Data is split across tables; `JOIN` brings them together temporarily.
- `ON` states under what condition two rows match.
- `INNER JOIN` returns only matches; `LEFT JOIN` keeps every row on the
  left.
- When both tables have a column of the same name, an alias is
  **required**.
- **`LEFT JOIN` + a `WHERE` on the right table = `INNER JOIN`.** Put the
  condition inside `ON`.
- To find non-matching rows: `LEFT JOIN ... WHERE right.column IS NULL`.
- A join can **multiply** rows; counting may need `DISTINCT`.
- After a `LEFT JOIN`, count a column from the right table rather than `*`.
