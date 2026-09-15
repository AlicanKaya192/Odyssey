# Window Functions

`GROUP BY` gathers rows together: twelve products come down to four
categories and the products themselves disappear. Most of the time you
need both — **the row itself and the information about the group it
belongs to.** "Where does this product rank in its category?", "Where
did the revenue get to with this order?", "When was the customer's
previous order?"

Window functions do exactly that: they add a calculation next to every
row **without gathering the rows**. The Advanced level starts here; the
schema is the eight-table order database of the Intermediate level, and
every result below was measured on it.

## GROUP BY and OVER

<figure class="fig">
  <div class="versus">
    <div>
      <h4>GROUP BY</h4>
      <pre><code>SELECT category_code, MAX(price)
FROM products
GROUP BY category_code;</code></pre>
      <p>4 rows: one row per category, the products are gone.</p>
    </div>
    <div>
      <h4>OVER</h4>
      <pre><code>SELECT name, category_code,
  MAX(price) OVER (
    PARTITION BY category_code)
FROM products;</code></pre>
      <p>12 rows: every product stays, with its category's highest price next to it.</p>
    </div>
  </div>
</figure>

Measured: 4 rows with `GROUP BY`, 12 with `PARTITION BY`.

Wherever you see `OVER`, there is a window function. The aggregate
functions you know (`SUM`, `COUNT`, `AVG`, `MAX`) become window functions
when written with `OVER`; and there are new functions that only work
with a window: `ROW_NUMBER`, `RANK`, `LAG`...

## Inside OVER

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">PARTITION BY</span><span class="anat-body">Splits the rows into groups; the calculation starts again in every group. Left out, the whole result is one group.</span></div>
    <div class="anat-row"><span class="anat-label">ORDER BY</span><span class="anat-body">The order inside the group. Row numbers, running totals and the previous row are worked out in this order.</span></div>
    <div class="anat-row"><span class="anat-label">ROWS ...</span><span class="anat-body">The frame: which of the group's rows go into the calculation. Left out, there is a default — the sneakiest trap of the section.</span></div>
  </div>
</figure>

All three are optional: `SUM(stock) OVER ()` writes the whole table's
total on every row.

## Row numbers: ROW_NUMBER, RANK, DENSE_RANK

```sql
SELECT name, stock,
       ROW_NUMBER() OVER (ORDER BY stock DESC) AS rn,
       RANK()       OVER (ORDER BY stock DESC) AS rk,
       DENSE_RANK() OVER (ORDER BY stock DESC) AS drk
FROM products
ORDER BY stock DESC, name;
```

Measured (a piece from the top and one from the bottom):

| name | stock | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|---|
| Antivirus | 99 | 1 | 1 | 1 |
| Office Suite | 99 | 2 | 1 | 1 |
| Cable | 60 | 3 | **3** | **2** |
| Keyboard | 32 | 4 | 4 | 3 |
| … | | | | |
| Mouse | 0 | 11 | 11 | 10 |
| Projector | 0 | 12 | 11 | 10 |

The three only differ **on ties**:

- `ROW_NUMBER` gives everyone a different number and splits ties too.
- `RANK` gives ties the same number and then **skips**: 1, 1, 3.
- `DENSE_RANK` does not skip: 1, 1, 2.

**Which of the tied rows comes first is not fixed.** The same
`ROW_NUMBER() OVER (ORDER BY stock DESC)` was run in two different
queries: in one Antivirus got number 1, in the other Office Suite. Not an
error, but not repeatable either. A column that tells them apart pins it
down: `ORDER BY stock DESC, name`.

`ROW_NUMBER() OVER ()`, on the other hand, is an error:
`The function 'ROW_NUMBER' must have an OVER clause with ORDER BY.`
A row number cannot be given without saying what it goes by.

## The best of each group

"The most expensive product in each category": `GROUP BY` with
`MAX(price)` finds the price but not the product's **name**. With a
window:

```sql
SELECT category_code, name, price
FROM (
    SELECT category_code, name, price,
           ROW_NUMBER() OVER (PARTITION BY category_code
                              ORDER BY price DESC) AS rn
    FROM products
) AS ranked
WHERE rn = 1;
```

| category_code | name | price |
|---|---|---|
| ACC | Microphone | 1320.00 |
| COM | Laptop | 24500.00 |
| DIS | Projector | 7400.00 |
| SOF | Office Suite | 2400.00 |

Why nested? Because both short cuts raise an error (measured):

| Written as | Result |
|---|---|
| `WHERE ROW_NUMBER() OVER (...) = 1` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` |
| `SELECT ..., ROW_NUMBER() OVER (...) AS rn ... WHERE rn = 1` | `Invalid column name 'rn'.` |

`WHERE` runs **before** `SELECT`; neither the number nor the alias exists
there yet. Once the numbered query goes inside `FROM (...)`, the outer
`WHERE` sees it as a ready-made column. The `WITH` of the next section
will write the same thing more readably.

## The running total

```sql
SELECT o.id, o.order_date,
       SUM(i.quantity * i.unit_price) AS total,
       SUM(SUM(i.quantity * i.unit_price))
           OVER (ORDER BY o.order_date) AS running_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY o.id, o.order_date
ORDER BY o.order_date;
```

`SUM(SUM(...))` looks odd at first: the inner `SUM` is the grouping's
total (the order's amount), the outer one is the window — it adds up the
amounts up to that date. Because the window runs **after** the grouping,
the two can be written together.

| id | order_date | total | running_total |
|---|---|---|---|
| 1001 | 2026-01-08 | 1815.00 | 1815.00 |
| 1002 | 2026-01-15 | 30900.00 | 32715.00 |
| 1003 | 2026-02-02 | 2340.00 | 35055.00 |
| … | | | |
| 1010 | 2026-04-17 | 5110.00 | 99165.00 |

## The frame trap

Write `OVER (ORDER BY ...)` without a frame and the server uses a
default: "from the start **up to this value**". Value, not row — rows
with the same value always go in together. If the order column has ties,
the running total goes quietly wrong. Measured, with order lines in
`order_id` order:

```sql
SUM(quantity * unit_price) OVER (ORDER BY order_id)                      -- default
SUM(quantity * unit_price) OVER (ORDER BY order_id ROWS UNBOUNDED PRECEDING)
```

| order_id | product_id | line | default | with `ROWS` |
|---|---|---|---|---|
| 1001 | 1 | 900.00 | **1815.00** | 900.00 |
| 1001 | 3 | 440.00 | **1815.00** | 1340.00 |
| 1001 | 9 | 475.00 | 1815.00 | 1815.00 |
| 1002 | 2 | 6400.00 | **32715.00** | 8215.00 |
| 1002 | 4 | 24500.00 | 32715.00 | 32715.00 |

With the default, all three lines of 1001 show 1815: all three counted as
"the same value". `ROWS` counts row by row. If the order among ties
matters too, add a column that tells them apart:
`ORDER BY order_id, product_id`.

How a frame is written:

| Frame | The rows that go in | Used for |
|---|---|---|
| `ROWS UNBOUNDED PRECEDING` | from the start up to this row | a running total |
| `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` | the previous row and this one | a moving average |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | the whole group | things like `LAST_VALUE` |

`RANGE` cannot take a number: `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW`
→ `RANGE is only supported with UNBOUNDED and CURRENT ROW window frame
delimiters.` (measured). To count rows, use `ROWS`.

## The previous and the next row: LAG, LEAD

Monthly revenue (without the cancelled ones) and the change against the
previous month:

```sql
SELECT month, revenue,
       LAG(revenue)  OVER (ORDER BY month) AS prev_revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change,
       LEAD(revenue) OVER (ORDER BY month) AS next_revenue
FROM (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)
) AS monthly
ORDER BY month;
```

| month | revenue | prev_revenue | change | next_revenue |
|---|---|---|---|---|
| 2026-01-01 | 32715.00 | NULL | NULL | 28680.00 |
| 2026-02-01 | 28680.00 | 32715.00 | −4035.00 | 7710.00 |
| 2026-03-01 | 7710.00 | 28680.00 | **−20970.00** | 30060.00 |
| 2026-04-01 | 30060.00 | 7710.00 | 22350.00 | NULL |

The first month has nothing before it: `LAG` gives `NULL`, and so does
the change. A third argument changes the value in that case:
`LAG(revenue, 1, 0)` gave `0.00` for January. The second argument is how
many rows back to look.

With `PARTITION BY`, every customer's own history:

```sql
SELECT customer_id, id, order_date,
       DATEDIFF(day,
                LAG(order_date) OVER (PARTITION BY customer_id
                                      ORDER BY order_date),
                order_date) AS gap_days
FROM orders
ORDER BY customer_id, order_date;
```

| customer_id | id | order_date | gap_days |
|---|---|---|---|
| 1 | 1001 | 2026-01-08 | NULL |
| 1 | 1003 | 2026-02-02 | 25 |
| 1 | 1006 | 2026-03-03 | 29 |
| 2 | 1002 | 2026-01-15 | NULL |
| 2 | 1008 | 2026-03-22 | 66 |

Without `PARTITION BY` every order would go into one line and the
"previous" of 1003 would be 1002 — another customer's order.

## A share of the total

`OVER ()` — an empty window — writes the whole result's total on every
row. With it a share is a single query:

```sql
SELECT p.category_code,
       SUM(i.quantity * i.unit_price) AS revenue,
       CAST(100.0 * SUM(i.quantity * i.unit_price)
            / SUM(SUM(i.quantity * i.unit_price)) OVER ()
            AS DECIMAL(5,2)) AS share
FROM order_items i
JOIN products p ON p.id = i.product_id
JOIN orders o ON o.id = i.order_id
WHERE o.status <> 'cancelled'
GROUP BY p.category_code
ORDER BY revenue DESC;
```

| category_code | revenue | share |
|---|---|---|
| COM | 67900.00 | 68.47 |
| DIS | 12800.00 | 12.91 |
| ACC | 12165.00 | 12.27 |
| SOF | 6300.00 | 6.35 |

All of them out of `99165.00` — the same number as the last row of the
running total. Forget the `WHERE` and SOF becomes `8700.00`: the Office
Suite (2400) of the cancelled order 1006 gets in.

## A few more tools

| Function | What it gives | Measured |
|---|---|---|
| `COUNT(*) OVER (PARTITION BY customer_id)` | The customer's number of orders, on each of their rows | 3 on row 1001 |
| `NTILE(4) OVER (ORDER BY price)` | Splits the rows into 4 equal groups | 12 products → 3 each |
| `NTILE(5) OVER (ORDER BY price)` | If they do not split evenly, the first groups are bigger | 3, 3, 2, 2, 2 |
| `FIRST_VALUE(name) OVER (ORDER BY price)` | The first value in the order | Cable on every ACC row |
| `AVG(stock) OVER ()` | On a whole-number column, **a whole number** | 19 for ACC (really 19.33) |

`LAST_VALUE`, however, falls into the frame trap: `LAST_VALUE(name) OVER
(ORDER BY price)` gave **the row's own name** on every row, because the
default frame ends at that row. To really get the last one, the frame
has to be opened up: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING` → Microphone on every row.

## Where a window can be written

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body">Yes. Its real home.</span></div>
    <div class="anat-row"><span class="anat-label">ORDER BY</span><span class="anat-body">Yes: <code>ORDER BY ROW_NUMBER() OVER (ORDER BY price DESC)</code> worked.</span></div>
    <div class="anat-row"><span class="anat-label">WHERE, UPDATE ... SET</span><span class="anat-body">No. Both: <code>Windowed functions can only appear in the SELECT or ORDER BY clauses.</code></span></div>
  </div>
</figure>

One last note: the `ORDER BY` inside `OVER` is only the order of **the
calculation**. For the order of the result's rows, a separate `ORDER BY`
goes at the end of the query. In the measurements the result sometimes
came back in the `OVER` order, but that is not a promise.

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">OVER</span><span class="anat-body">Adds a calculation to every row without gathering the rows.</span></div>
    <div class="anat-row"><span class="anat-label">Row numbers</span><span class="anat-body"><code>ROW_NUMBER</code> / <code>RANK</code> / <code>DENSE_RANK</code>; on ties, add a column that tells rows apart.</span></div>
    <div class="anat-row"><span class="anat-label">First of a group</span><span class="anat-body"><code>PARTITION BY</code>, an inner query, <code>WHERE rn = 1</code> outside.</span></div>
    <div class="anat-row"><span class="anat-label">Running total</span><span class="anat-body"><code>SUM(...) OVER (ORDER BY ... ROWS UNBOUNDED PRECEDING)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Previous row</span><span class="anat-body"><code>LAG</code>; the next one <code>LEAD</code>; <code>NULL</code> on the first row.</span></div>
    <div class="anat-row"><span class="anat-label">Share</span><span class="anat-body"><code>x / SUM(x) OVER ()</code>.</span></div>
  </div>
</figure>

The next section is `WITH`: giving a name to the `FROM (...) AS ranked`
pattern you wrote again and again in this section.
