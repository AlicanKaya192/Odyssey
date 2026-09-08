A one-page summary of the subquery forms. The results were measured on
this section's eight-table schema.

## Where they can go

| Place | What it must return | Example |
|---|---|---|
| `WHERE` (comparison) | a single value | `price > (SELECT AVG(price) ...)` |
| `WHERE` (`IN`) | one column, many rows | `code IN (SELECT ...)` |
| `WHERE` (`EXISTS`) | does not matter | `EXISTS (SELECT 1 ...)` |
| `SELECT` | **one row, one column** | `(SELECT COUNT(*) ...) AS n` |
| `FROM` | a table — **alias required** | `FROM (SELECT ...) t` |
| `HAVING` | a single value | `HAVING COUNT(*) > (SELECT ...)` |

If a subquery inside `SELECT` returns more than one row, the error is
`Subquery returned more than 1 value`.

## Correlated or not

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Not correlated</span><span class="anat-body">It <b>does not</b> mention an alias from the outer query. It runs once and its result is the same for every row. It can be run on its own.</span></div>
    <div class="anat-row"><span class="anat-label">Correlated</span><span class="anat-body">It <b>does</b> mention an alias from the outer query. It runs again for every outer row. It cannot be run on its own.</span></div>
  </div>
</figure>

The practical way to tell: copy the subquery and run it alone. If it
works it is not correlated; if it says "invalid column name" it is.

## EXISTS and NOT EXISTS

```sql
-- customers who have ordered (5 rows)
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)

-- customers who never ordered (1 row)
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
```

Three details:

- **What you select inside does not matter.** `SELECT 1`, `SELECT *`,
  `SELECT name` — all the same. Writing `1` is the convention.
- **It stops early.** It stops as soon as it finds a row; it does not
  count.
- **It is unaffected by empty values.** The `NOT IN` trap does not apply.

## The NOT IN trap

Measured:

| Query | Result | Correct |
|---|---|---|
| `code NOT IN (SELECT supplier_code FROM products)` | **0 rows** | 1 |
| the same with `WHERE supplier_code IS NOT NULL` added | 1 row | 1 |
| `NOT EXISTS (...)` | 1 row | 1 |

The reason: three products have an empty `supplier_code`, so the list
contains `NULL`. `NOT IN` turns into this chain:

```
code <> 'S1' AND code <> 'S2' AND ... AND code <> NULL
                                          ^^^^^^^^^^^^ always unknown
```

While one part of an `AND` chain is unknown, the result can never be true.

**The rule: do not write `NOT IN` with a subquery — write `NOT EXISTS`.**

The positive `IN` does not have this problem: it is an `OR` chain and one
true part is enough.

## An empty subquery

| Query | Result |
|---|---|
| `IN (empty subquery)` | no rows |
| `NOT IN (empty subquery)` | **every row** |
| `EXISTS (empty subquery)` | no rows |
| `NOT EXISTS (empty subquery)` | every row |

When the subquery comes back empty, `NOT IN` is safe — the problem only
appears when the list contains `NULL`.

## The derived table

```sql
SELECT t.customer_id, t.order_count
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders GROUP BY customer_id
) t
WHERE t.order_count >= 2;
```

- **The alias is required.** Without `) t` it is a syntax error.
- Every column of the inner query **must have a name**; calculated columns
  are named with `AS`.
- In simple cases `HAVING` is shorter. The derived table becomes the only
  way when the grouped result has to be **joined to another table**.

## Subquery or JOIN

| What you need | Choose |
|---|---|
| A column from another table | `JOIN` |
| Only to filter | `EXISTS` / `IN` |
| To find non-matches | `NOT EXISTS` |
| A single number (average, total) | a scalar subquery |
| To group and then join | a derived table |

On speed they are usually the same: the server can turn most subqueries
into joins. The one real difference is row multiplication — a `JOIN` can
multiply rows and `EXISTS` cannot.
