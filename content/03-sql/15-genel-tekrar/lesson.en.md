# Overall Review

Fifteen sections ago you installed SQL Server and wrote your first
`SELECT`. Now you can answer all kinds of questions from an order
database, create tables and put rules on them, measure why a query is
slow and put code inside the database.

This section teaches nothing new. It gathers, in one place and with
measured numbers, **the order** in which a query runs and the most
common traps of the path. Everything was measured on the eight-table
schema of the Intermediate level.

## The order a query runs in

The order you write is `SELECT ... FROM ... WHERE ...`. The order the
server runs it in is different:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1</b><br>FROM<br>JOIN</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>WHERE</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>3</b><br>GROUP BY</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>HAVING</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>SELECT<br>windows</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>ORDER BY</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>7</b><br>TOP</span>
  </div>
  <figcaption>A step cannot see what a later step produces.</figcaption>
</figure>

Most of the errors you met on the path come from this order (measured):

| Written as | Result | Why |
|---|---|---|
| `SELECT name AS n ... WHERE n = 'Mouse'` | `Invalid column name 'n'.` | `WHERE` (2) comes before `SELECT` (5) |
| `SELECT price * 2 AS double_price ... WHERE double_price > 1000` | `Invalid column name 'double_price'.` | the same |
| `SELECT category_code AS cc ... GROUP BY cc` | `Invalid column name 'cc'.` | `GROUP BY` (3) comes before `SELECT` |
| `WHERE COUNT(*) > 1` | `An aggregate may not appear in the WHERE clause ...` | aggregation comes after grouping; the condition goes into `HAVING` |
| `WHERE ROW_NUMBER() OVER (...) <= 3` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` | windows are worked out in `SELECT` |
| `SELECT category_code, name, COUNT(*) ... GROUP BY category_code` | `Column 'products.name' is invalid in the select list ...` | after grouping there is no single `name` per row |
| `SELECT price AS p ... ORDER BY p` | worked | `ORDER BY` (6) comes after `SELECT` |
| `ORDER BY 2` | worked | by the second column |

If something a later step produces is needed in an earlier step, the
query goes one level in: `FROM (...)` or `WITH`.

## NULL: the unknown

Two orders in the `orders` table have no employee (`employee_id` is
`NULL`). Measured:

| Query | Result |
|---|---|
| `WHERE employee_id = NULL` | 0 rows |
| `WHERE employee_id IS NULL` | 2 |
| `WHERE employee_id <> 3` | 4 — the two `NULL` orders are neither "3" nor "not 3" |
| `COUNT(*)` / `COUNT(employee_id)` | 10 / 8 |
| `COUNT(*)` / `SUM(...)` over an empty set | 0 / `NULL` |
| `id NOT IN (SELECT employee_id FROM orders)` | **0 employees** |
| the same question with `NOT EXISTS` | 4 employees |

The `NOT IN` result is the sneakiest trap of the path. `x NOT IN (3, 4,
NULL)` really means "`x <> 3` and `x <> 4` and `x <> NULL`"; the last one
is never true, so the whole condition is true on no row. The fix is `NOT
EXISTS`, or `WHERE employee_id IS NOT NULL` in the subquery — both gave 4.

## Quietly turning a LEFT JOIN into an inner one

"Every customer and their shipped orders":

| Where the condition is | Rows | Customers |
|---|---|---|
| `LEFT JOIN orders o ON o.customer_id = c.id` + `WHERE o.status = 'shipped'` | 6 | 4 |
| `LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'shipped'` | 8 | 6 |

`WHERE` runs after the join: the `NULL` rows of unmatched customers
cannot pass `o.status = 'shipped'` and drop out. You wrote `LEFT JOIN`,
but the result is an inner join's. A condition on the right-hand table
goes into `ON`.

## When rows multiply

Joining `orders` with `order_items` gave **20 rows** for 10 orders.
`COUNT(o.customer_id)` gave 20, `COUNT(DISTINCT o.customer_id)` 5. After
the join every row is a **line**; counting or adding up something that
belongs to the order repeats it once per line.

The same question with `UNION`: customer and supplier cities gave 5 with
`UNION` and 10 with `UNION ALL`.

## Numbers

| Expression | Result |
|---|---|
| `7 / 2` | `3` — two whole numbers, a whole-number result |
| `7 / 2.0` | `3.500000` |
| `7 % 2` | `1` |
| `10 / 0` | `Divide by zero error encountered.` |
| `10 / NULLIF(0, 0)` | `NULL` |
| `CAST('abc' AS INT)` | `Conversion failed when converting the varchar value 'abc' to data type int.` |
| `TRY_CAST('abc' AS INT)` | `NULL` |
| `LEN('abc  ')` / `DATALENGTH('abc  ')` | `3` / `5` — `LEN` does not count trailing spaces |

## Changing and building

| Situation | Measured |
|---|---|
| `UPDATE products SET stock = stock` without `WHERE` | 12 rows affected — all of them |
| foreign keys in this schema | none (0) |
| deleting customer 1 (in a transaction that was rolled back) | deleted; 3 of their orders were left orphaned |
| `INSERT INTO categories VALUES ('XYZ')` | `Column name or number of supplied values does not match table definition.` |
| `WHERE id = (SELECT ... )` when the subquery returns 3 rows | `Subquery returned more than 1 value ...` |

In a schema without foreign keys, deleting and updating protect nothing.
That is exactly what the rules of the ninth section are for.

## The most common traps of the Advanced level

| Trap | Measured | Fix |
|---|---|---|
| `ROW_NUMBER` on ties | the same window gave a different number 1 in two queries | a column that tells rows apart |
| the default frame | all three lines of 1001 showed 1815 | `ROWS UNBOUNDED PRECEDING` |
| text in recursion | `Types don't match between the anchor and the recursive part` | `CAST` in both parts |
| a function on an indexed column | 42 reads instead of 2 | leave the column bare |
| a `SELECT *` view | the new column did not show up | name the columns |
| `OUTPUT` forgotten in the call | `NULL`, no error | `OUTPUT` in the definition and the call |

## Which tool for which question

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">"The rows that meet this condition"</span><span class="anat-body"><code>WHERE</code> — for <code>NULL</code>, <code>IS NULL</code></span></div>
    <div class="anat-row"><span class="anat-label">"One number per group"</span><span class="anat-body"><code>GROUP BY</code>; the group's condition in <code>HAVING</code></span></div>
    <div class="anat-row"><span class="anat-label">"Keep the row, add the group's information"</span><span class="anat-body"><code>OVER (PARTITION BY ...)</code></span></div>
    <div class="anat-row"><span class="anat-label">"Information from another table"</span><span class="anat-body"><code>JOIN</code>; keep the unmatched too: <code>LEFT JOIN</code>, condition in <code>ON</code></span></div>
    <div class="anat-row"><span class="anat-label">"Work this out first, then use it"</span><span class="anat-body"><code>WITH</code></span></div>
    <div class="anat-row"><span class="anat-label">"A tree of unknown depth, a series in no table"</span><span class="anat-body">recursive <code>WITH</code></span></div>
    <div class="anat-row"><span class="anat-label">"The same query every day"</span><span class="anat-body"><code>VIEW</code>; work with parameters and rules: <code>PROCEDURE</code></span></div>
    <div class="anat-row"><span class="anat-label">"It is slow"</span><span class="anat-body">measure the reads; leave the column bare; an index</span></div>
    <div class="anat-row"><span class="anat-label">"This must never happen"</span><span class="anat-body"><code>NOT NULL</code>, <code>CHECK</code>, <code>FOREIGN KEY</code>, <code>UNIQUE</code></span></div>
  </div>
</figure>

## The exercises

Each of the five exercises combines several sections: a category's share
within a month (joins, grouping, dates, `WITH`, windows), returning
customers (`HAVING`, dates), a team's revenue (recursion, `LEFT JOIN`),
an order summary view (`LEFT JOIN`, `COALESCE`, views) and a returns
table (table design, rules, adding data).

The SQL path ends here. The notes hold the whole path on one page and
what you can look at from here on.
