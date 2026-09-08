# Subqueries

You want to use one query's answer inside another: "products above the
average price", "products never sold", "the customer with the most
orders".

All of these are two steps: work something out first, then filter by it. A
**subquery** puts those two steps into one query.

## The simplest form: a single value

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

The query in parentheses produces **a single number**, and the outer query
uses it like a constant. The result is three rows.

This is called a **scalar subquery**: one row, one column.

You could do it in two steps — find the average, then type it in — but
then the query would be wrong as soon as the data changed. A subquery
works it out again on every run.

### It can go inside SELECT too

```sql
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
FROM customers c;
```

The inner query runs again **for every row of the outer query**: `c.id` is
a different customer each time.

This is called a **correlated subquery** — it depends on the outer row, so
it cannot be run on its own.

You get the same result with `LEFT JOIN` + `GROUP BY`. Which to choose
comes up shortly.

## Choosing from a list: IN

In the third section you wrote the list by hand. It can come from a query
instead:

```sql
SELECT name
FROM products
WHERE supplier_code IN (SELECT code FROM suppliers WHERE country = 'Turkey');
```

The inner query can return several rows, and `IN` expects a list anyway.

## The trap: NOT IN and empty values

You saw this trap in the third section, but there you wrote the list
yourself and would not put a `NULL` in it. **When the list comes from a
query, things change.**

The question "suppliers with no products":

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Returns nothing</h4>
      <pre><code>SELECT name FROM suppliers
WHERE code NOT IN (
  SELECT supplier_code
  FROM products);</code></pre>
    </div>
    <div class="ok">
      <h4>Returns the right answer</h4>
      <pre><code>SELECT name FROM suppliers s
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE p.supplier_code = s.code);</code></pre>
    </div>
  </div>
  <figcaption>The left one returns zero rows and the right one returns one (Rhine Components). The reason: three products have an empty supplier_code, so the subquery's list contains NULL, and NOT IN can never be true in that case.</figcaption>
</figure>

No error and no warning — the query runs and says "there is no supplier
without products". But there is.

There are two fixes:

```sql
-- 1. clean the list
WHERE code NOT IN (
  SELECT supplier_code FROM products WHERE supplier_code IS NOT NULL)

-- 2. use NOT EXISTS
WHERE NOT EXISTS (
  SELECT 1 FROM products p WHERE p.supplier_code = s.code)
```

The second is preferred: `NOT EXISTS` is unaffected by empty values and
states the intent more clearly.

## EXISTS: is there any?

`EXISTS` answers one question: "does the inner query return **at least
one** row?"

```sql
SELECT name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

Customers who have ordered — five rows.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT 1</span><span class="anat-body">What is selected <b>does not matter</b>. <code>EXISTS</code> looks at whether a row exists, not at its contents. Writing <code>1</code> is the convention.</span></div>
    <div class="anat-row"><span class="anat-label">Correlated</span><span class="anat-body">The inner query uses <code>c.id</code>; it runs again for every row of the outer query.</span></div>
    <div class="anat-row"><span class="anat-label">Stops early</span><span class="anat-body">It stops as soon as it finds one row; it does not count them all.</span></div>
  </div>
</figure>

`NOT EXISTS` is the opposite: "is there no row at all?" It is the safest
way to find non-matching rows.

## A subquery as a table: the derived table

A subquery can also sit inside `FROM`, where it behaves like a temporary
table:

```sql
SELECT t.category_code, t.n
FROM (
    SELECT category_code, COUNT(*) AS n
    FROM products
    GROUP BY category_code
) t
WHERE t.n > 2;
```

**The alias is required.** Leave out the `t` and you get a syntax error;
the server wants this temporary table to have a name.

The pattern is used for "filtering the result of a grouping again". In
simple cases `HAVING` is shorter, but when the grouped result has to be
**joined to another table**, a derived table is the only way.

## Correlated or not?

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>Not correlated</h4>
      <pre><code>WHERE price > (
  SELECT AVG(price)
  FROM products)</code></pre>
      <p>Runs once; the result is the same for everyone.</p>
    </div>
    <div class="ok">
      <h4>Correlated</h4>
      <pre><code>WHERE p.price > (
  SELECT AVG(p2.price)
  FROM products p2
  WHERE p2.category_code =
        p.category_code)</code></pre>
      <p>Runs again for every row; it depends on the outer row.</p>
    </div>
  </div>
  <figcaption>The left one is "products above the average" (3 rows), the right one "products above their own category's average" (6 rows). Two different questions.</figcaption>
</figure>

You cannot run a correlated subquery on its own: it refers to an alias
from the outer query.

## Subquery or JOIN?

Most questions can be answered either way. The choice is about
readability:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Adding a column</span><span class="anat-body"><b>JOIN.</b> Bringing a column from another table is what `JOIN` is for.</span></div>
    <div class="anat-row"><span class="anat-label">Only filtering</span><span class="anat-body"><b>EXISTS</b> or <b>IN</b>. You are not taking a column, so there is no need to join and no risk of multiplying rows.</span></div>
    <div class="anat-row"><span class="anat-label">Looking for non-matches</span><span class="anat-body"><b>NOT EXISTS.</b> <code>LEFT JOIN ... IS NULL</code> works too, but <code>NOT EXISTS</code> states the intent more clearly.</span></div>
    <div class="anat-row"><span class="anat-label">Needing a single number</span><span class="anat-body"><b>A scalar subquery.</b> An average, a total, a maximum.</span></div>
  </div>
</figure>

**On speed** there is usually no difference: the server can turn both into
the same plan. "Subqueries are slow" is a common saying that is no longer
true.

The one real difference is row multiplication: a `JOIN` can multiply rows
and `EXISTS` cannot. If you only want to filter, `EXISTS` is safer for
that reason.

## Where can a subquery go?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">WHERE</span><span class="anat-body">The most common place. With <code>IN</code>, <code>EXISTS</code> or a comparison.</span></div>
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body">As a calculated column. It must return a single value.</span></div>
    <div class="anat-row"><span class="anat-label">FROM</span><span class="anat-body">A derived table. The alias is required.</span></div>
    <div class="anat-row"><span class="anat-label">HAVING</span><span class="anat-body">As a threshold in a group condition.</span></div>
  </div>
</figure>

A subquery inside `SELECT` must return **one row and one column**. If it
returns more, the server raises an error:
`Subquery returned more than 1 value`.

## Summary

- A subquery is a query inside a query, written in parentheses.
- A **scalar** subquery returns a single value and is used like a
  constant.
- `IN (SELECT ...)` takes the list from a query.
- **`NOT IN` with a subquery is dangerous:** a single `NULL` in the list
  makes the result always empty. Use `NOT EXISTS`.
- `EXISTS` asks "is there at least one row"; what it selects does not
  matter.
- A subquery in `FROM` is a temporary table and **its alias is required**.
- A **correlated** subquery depends on the outer row and runs again for
  each one.
- Use `JOIN` to bring columns, `EXISTS` to filter only.
