# WITH and Recursion

In the previous section you wrote the same pattern again and again:
putting a query inside `FROM (...)` and filtering outside. It works, but
it is hard to read — the query reads from the inside out and the inner
query's name comes at the very end.

`WITH` gives that inner query a name **at the start**. The query reads
from the top down: first "prepare this", then "use what you prepared".
And it can do one thing that `FROM (...)` cannot do at all: **refer to
itself.** That is how a management tree of unknown depth, or months that
appear in no table, come out of a single query.

Every result below was measured on the eight-table schema of the
Intermediate level.

## WITH: giving a query a name

<figure class="fig">
  <div class="versus">
    <div>
      <h4>FROM (...)</h4>
      <pre><code>SELECT category_code, name
FROM (
  SELECT category_code, name,
    ROW_NUMBER() OVER (
      PARTITION BY category_code
      ORDER BY price DESC) AS rn
  FROM products
) AS ranked
WHERE rn = 1;</code></pre>
      <p>Inside out: the name comes last.</p>
    </div>
    <div>
      <h4>WITH</h4>
      <pre><code>WITH ranked AS (
  SELECT category_code, name,
    ROW_NUMBER() OVER (
      PARTITION BY category_code
      ORDER BY price DESC) AS rn
  FROM products
)
SELECT category_code, name
FROM ranked
WHERE rn = 1;</code></pre>
      <p>Top down: first the name, then its use.</p>
    </div>
  </div>
</figure>

Both brought back the same four products (measured): Microphone,
Laptop, Projector, Office Suite. What `WITH` defines is called a **CTE**
(*common table expression*): a named query that lives only for the
length of that statement.

## Using one name twice

An inner query written with `FROM (...)` can be used once. A CTE's name
as often as you like. "Customers who spend above the average":

```sql
WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(i.quantity * i.unit_price) AS total
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.customer_id
)
SELECT c.name, ct.total
FROM customer_totals ct
JOIN customers c ON c.id = ct.customer_id
WHERE ct.total > (SELECT AVG(total) FROM customer_totals)
ORDER BY ct.total DESC;
```

| name | total |
|---|---|
| Helix Studio | 49690.00 |
| Bright Office | 34100.00 |

`customer_totals` appears in two places: as the source of the rows and
inside the average. The average of the five customers is `19833.00`; two
stay above it. Without `WITH` the same grouping would be written twice.

## A chain: more than one CTE

CTEs are separated by commas, and each can use **the ones before it**:

```sql
WITH order_totals AS (
    SELECT o.id, o.employee_id,
           SUM(i.quantity * i.unit_price) AS total
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.id, o.employee_id
),
employee_totals AS (
    SELECT employee_id, COUNT(*) AS orders, SUM(total) AS revenue
    FROM order_totals
    WHERE employee_id IS NOT NULL
    GROUP BY employee_id
)
SELECT e.name, et.orders, et.revenue
FROM employee_totals et
JOIN employees e ON e.id = et.employee_id
ORDER BY et.revenue DESC;
```

| name | orders | revenue |
|---|---|---|
| Deniz Kaya | 4 | 36700.00 |
| Ceren Aksoy | 3 | 35915.00 |

Each step can be read on its own: first the order amounts, then the
employee totals, finally the names. Since two aggregations cannot be
nested (`SUM(SUM(...))` only works with a window), two steps are needed
here.

## The rules

Measured:

| Written as | Result |
|---|---|
| `WITH` without a semicolon after `SET NOCOUNT ON` | `Incorrect syntax near the keyword 'with'. ... the previous statement must be terminated with a semicolon.` |
| `WITH` without a semicolon after `SELECT ... FROM products` | `Incorrect syntax near 'x'. If this is intended to be a common table expression, you need to explicitly terminate the previous statement with a semi-colon.` |
| the previous statement ends with `;` | works |
| `;WITH ...` | works |
| using the CTE in a second statement | `Invalid object name 'x'.` |
| `ORDER BY` inside a CTE | `The ORDER BY clause is invalid in ... common table expressions, unless TOP, OFFSET or FOR XML is also specified.` |
| `WITH a AS (... FROM b), b AS (...)` | `Invalid object name 'b'.` |
| two CTEs with the same name | `Duplicate common table expression name 'a' was specified.` |
| `WITH` inside a CTE | a syntax error |
| `WITH x (product, cost) AS (...)` | names the columns; works |

The first two are the ones you meet most: because the word `WITH` is
used for other jobs in T-SQL too, the server wants to know that the
previous statement has ended. Make a habit of ending the previous
statement with `;`. In this application code that starts with `WITH` —
even with a comment before it — runs fine (measured).

## Recursion: a CTE that refers to itself

Every employee in the `employees` table has a `manager_id`. To answer
"what level is everyone at?" you do not need to know how many levels
there are:

```sql
WITH chain AS (
    SELECT id, name, 0 AS level          -- the start
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, c.level + 1     -- the part that refers to itself
    FROM employees e
    JOIN chain c ON e.manager_id = c.id
)
SELECT id, name, level FROM chain ORDER BY level, id;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">The start</span><span class="anat-body">The query before <code>UNION ALL</code>. It runs once: Ada, who has no manager.</span></div>
    <div class="anat-row"><span class="anat-label">UNION ALL</span><span class="anat-body">Joins the two parts. <code>UNION</code> cannot be used in recursion.</span></div>
    <div class="anat-row"><span class="anat-label">The self-referring part</span><span class="anat-body">The CTE's own name appears in its <code>FROM</code>. At every step it works with the rows that were <strong>new</strong> in the previous step.</span></div>
    <div class="anat-row"><span class="anat-label">Stopping</span><span class="anat-body">When the part returns no rows, the recursion ends.</span></div>
  </div>
</figure>

Step by step:

<figure class="fig">
  <div class="flow">
    <span class="node acc">0 · Ada</span>
    <span class="arrow">→</span>
    <span class="node">1 · Bora, Emre</span>
    <span class="arrow">→</span>
    <span class="node">2 · Ceren, Deniz, Fulya</span>
    <span class="arrow">→</span>
    <span class="node no">3 · nobody, stop</span>
  </div>
</figure>

| id | name | level |
|---|---|---|
| 1 | Ada Kilic | 0 |
| 2 | Bora Yilmaz | 1 |
| 5 | Emre Sahin | 1 |
| 3 | Ceren Aksoy | 2 |
| 4 | Deniz Kaya | 2 |
| 6 | Fulya Demir | 2 |

Write `UNION` and you get an error: `Recursive common table expression
'chain' does not contain a top-level UNION ALL operator.`

## Writing the path: the type trap

Writing the chain itself instead of the level — `Ada Kilic > Bora
Yilmaz > Ceren Aksoy` — is the same structure, but the first attempt
raises an error (measured):

```sql
SELECT id, name AS path ...                -- the start
SELECT e.id, c.path + N' > ' + e.name ...  -- the self-referring part
```

`Types don't match between the anchor and the recursive part in column
"path" of recursive query "chain".`

The `name` column is `NVARCHAR(40)`; the joined path is a longer type.
The server wants the same type in both parts. The fix is to convert both
to the same type:

```sql
SELECT id, CAST(name AS NVARCHAR(200)) AS path ...
SELECT e.id, CAST(c.path + N' > ' + e.name AS NVARCHAR(200)) ...
```

| id | path |
|---|---|
| 1 | Ada Kilic |
| 2 | Ada Kilic > Bora Yilmaz |
| 3 | Ada Kilic > Bora Yilmaz > Ceren Aksoy |
| 6 | Ada Kilic > Emre Sahin > Fulya Demir |

## Going up

The same structure works the other way too. From Fulya up to the top:

```sql
WITH up AS (
    SELECT id, name, manager_id, 0 AS step
    FROM employees WHERE id = 6
    UNION ALL
    SELECT e.id, e.name, e.manager_id, u.step + 1
    FROM employees e
    JOIN up u ON e.id = u.manager_id
)
SELECT step, name FROM up ORDER BY step;
```

Result: Fulya Demir (0), Emre Sahin (1), Ada Kilic (2). The only
difference is in the join: going down it is `e.manager_id = c.id`
("those whose manager is in the chain"), going up `e.id = u.manager_id`
("the manager of the one in the chain"). With the direction reversed,
the downward query brought back only Ada.

## Against endless loops: MAXRECURSION

A recursion with no stopping condition would go on forever. By default
the server cuts it off **at 100 steps**. Measured with a counter that
starts at 1 and goes up by one:

| Query | Result |
|---|---|
| `... WHERE k < 101` | 101 rows |
| `... WHERE k < 102` | `The statement terminated. The maximum recursion 100 has been exhausted before statement completion.` |
| `... WHERE k < 200` + `OPTION (MAXRECURSION 200)` | 200 rows |
| `... WHERE k < 1000` + `OPTION (MAXRECURSION 0)` | 1000 rows — `0` removes the limit |
| `OPTION (MAXRECURSION 40000)` | an error: 32767 at most |
| no `WHERE` + `OPTION (MAXRECURSION 50)` | stopped at 50 with an error |

`OPTION` goes not inside the CTE but at **the very end of the statement**
that uses it; written inside, it was a syntax error. The limit is a
safety net: a real tree is not 100 levels deep, and a chain of command
longer than 100 is most likely a mistake in the data.

## Rows that are in no table

Monthly revenue only shows the months that have orders. If "every month
from January to June" is needed, the months are generated first:

```sql
WITH months AS (
    SELECT CAST('2026-01-01' AS DATE) AS month
    UNION ALL
    SELECT DATEADD(month, 1, month)
    FROM months
    WHERE month < '2026-06-01'
),
revenue AS (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)
)
SELECT m.month, COALESCE(r.revenue, 0) AS revenue
FROM months m
LEFT JOIN revenue r ON r.month = m.month
ORDER BY m.month;
```

| month | revenue |
|---|---|
| 2026-01-01 | 32715.00 |
| 2026-02-01 | 28680.00 |
| 2026-03-01 | 7710.00 |
| 2026-04-01 | 30060.00 |
| 2026-05-01 | **0.00** |
| 2026-06-01 | **0.00** |

Two details change the result (measured): with `JOIN` instead of `LEFT
JOIN`, May and June dropped out (4 rows); without `COALESCE` those two
months came back as `NULL`.

## What recursion does not allow

Two things cannot be written in the self-referring part (measured):

| Written as | Error |
|---|---|
| `MAX(k)`, `GROUP BY`, `HAVING` | `GROUP BY, HAVING, or aggregate functions are not allowed in the recursive part of a recursive common table expression` |
| `LEFT JOIN` | `Outer join is not allowed in the recursive part of a recursive common table expression` |

If an aggregation is needed, it is done **outside** the CTE. "How many
people are below each employee, directly or indirectly?" — the
recursion lists who is below each root, and the counting happens in the
`GROUP BY` outside:

```sql
WITH r AS (
    SELECT id AS root, id FROM employees
    UNION ALL
    SELECT r.root, e.id
    FROM employees e
    JOIN r ON e.manager_id = r.id
)
SELECT root, COUNT(*) - 1 AS below
FROM r
GROUP BY root;
```

Result: Ada 5, Bora 2, Emre 1, everyone else 0. (The `- 1` takes out the
person themselves.)

## Changing data with WITH

A CTE can be written before a `DELETE` or an `UPDATE` just as before a
`SELECT` — and the change goes to **the underlying table**. The
well-known way of cleaning out duplicate records:

```sql
WITH d AS (
    SELECT email,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY email) AS rn
    FROM #dup
)
DELETE FROM d WHERE rn > 1;
```

On a six-row table (`a` twice, `b` once, `c` three times) **3 rows** were
deleted and one of each address was left (measured). In the same way,
`WITH cheap AS (SELECT TOP 2 ... ORDER BY price) UPDATE cheap SET stock =
stock + 100` changed the stock of the two cheapest products (Cable,
Mouse) in the `products` table (the measurement was made inside a
transaction that was rolled back).

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">WITH name AS (...)</span><span class="anat-body">Gives a query a name; the name is valid only for that statement.</span></div>
    <div class="anat-row"><span class="anat-label">More than one</span><span class="anat-body">With commas; each sees the ones before it.</span></div>
    <div class="anat-row"><span class="anat-label">Semicolon</span><span class="anat-body">The statement before <code>WITH</code> must end with <code>;</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Recursion</span><span class="anat-body">The start + <code>UNION ALL</code> + the self-referring part; it stops when no new rows come.</span></div>
    <div class="anat-row"><span class="anat-label">Type</span><span class="anat-body">Column types must match in both parts: <code>CAST</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Limit</span><span class="anat-body">100 steps by default; <code>OPTION (MAXRECURSION n)</code> at the end of the statement.</span></div>
  </div>
</figure>

The next section is indexes: why the same query is sometimes slow, and
how the server finds a row.
