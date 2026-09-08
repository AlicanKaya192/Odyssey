The same question can be asked in three different ways. This note shows
which to pick and when — all three were measured on this section's schema.

## Question: customers with no orders

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NOT EXISTS</span><span class="anat-body"><b>Preferred.</b> It states the intent directly, empty values do not affect it, and it does not multiply rows.</span></div>
    <div class="anat-row"><span class="anat-label">LEFT JOIN + IS NULL</span><span class="anat-body">Works, and common. Being two steps, it is less obvious at a glance what it is asking.</span></div>
    <div class="anat-row"><span class="anat-label">NOT IN</span><span class="anat-body"><b>Avoided.</b> One single empty value in the list and it quietly returns nothing.</span></div>
  </div>
</figure>

```sql
-- 1. NOT EXISTS
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 2. LEFT JOIN
SELECT c.name FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- 3. NOT IN  (works on this data because customer_id is never empty,
--             but the same form on supplier_code returns nothing)
SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
```

All three give the same answer on this data. But the third one depends on
**the current state of the data**: the day `orders.customer_id` becomes a
column that can be empty, the query breaks silently.

**The rule: if you are asking a negative question, write `NOT EXISTS`.**

## Question: the order count of every customer

```sql
-- 1. LEFT JOIN + GROUP BY
SELECT c.name, COUNT(o.id) AS n
FROM customers c LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;

-- 2. scalar subquery
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS n
FROM customers c;
```

Both give the same answer (six rows, 0 for Quiet Partners).

- If you are adding **a single number**, the subquery reads better: you do
  not write `GROUP BY` and you do not think about what grouping does to the
  other columns.
- If you are adding **several numbers at once**, `JOIN` + `GROUP BY` is
  better: a separate subquery for each gets long and repetitive.

## Question: rows above the average of their own group

With this section's tools, only a **correlated subquery** can answer this:

```sql
SELECT p.name FROM products p
WHERE p.price > (
    SELECT AVG(p2.price) FROM products p2
    WHERE p2.category_code = p.category_code);
```

To solve it with `JOIN` you first build a derived table that produces the
category averages, then join to it:

```sql
SELECT p.name
FROM products p
JOIN (SELECT category_code, AVG(price) AS avg_price
      FROM products GROUP BY category_code) a
  ON a.category_code = p.category_code
WHERE p.price > a.avg_price;
```

The second is longer but usually faster on large tables: the averages are
worked out once, not again for every row.

At the advanced level there is a third and more readable way: **window
functions**.

## The decision, in short

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Bring a column</span><span class="anat-body"><code>JOIN</code></span></div>
    <div class="anat-row"><span class="anat-label">Ask whether it exists</span><span class="anat-body"><code>EXISTS</code></span></div>
    <div class="anat-row"><span class="anat-label">Ask whether it does not</span><span class="anat-body"><code>NOT EXISTS</code> — <b>never</b> <code>NOT IN</code></span></div>
    <div class="anat-row"><span class="anat-label">Work out one number</span><span class="anat-body">a scalar subquery</span></div>
    <div class="anat-row"><span class="anat-label">Group, then join</span><span class="anat-body">a derived table</span></div>
  </div>
</figure>

## A note on readability

Subqueries become unreadable once they nest. If you are nesting more than
three levels deep, you almost certainly need to break the query up.

The advanced level has the tool for that: `WITH` (the common table
expression). It does the same work, but written top to bottom as named
steps.
