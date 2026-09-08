The problems you will hit while writing `JOIN`. The first two raise
errors; the other four are **silent** and make the numbers wrong.

## Ambiguous column name 'X'

Both tables have a column with that name and you did not say which one you
meant.

```sql
SELECT name FROM products p JOIN categories c ON p.category_code = c.code;
-- Ambiguous column name 'name'
```

In this schema the `name` column exists in **five** tables: `categories`,
`suppliers`, `products`, `customers` and `employees`.

The fix is an alias: `p.name`, `c.name`. When working with several tables,
**putting an alias in front of every column** is a good habit — the query
does not break when a `JOIN` is added later.

## The multi-part identifier could not be bound

You used an alias that does not exist:

```sql
FROM products p JOIN categories c ON prd.category_code = c.code
```

No alias called `prd` was defined. It usually comes from renaming an alias
and forgetting to update one place.

---

## The silent mistakes

### 1. A WHERE that kills the LEFT JOIN

The most common mistake of all.

```sql
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code
WHERE s.country = 'Turkey'      -- 9 rows
```

On rows where the right side came back empty, `s.country` is `NULL`, and
because `NULL = 'Turkey'` is "unknown" the `WHERE` drops them. The
`LEFT JOIN` quietly becomes an `INNER JOIN`.

Written inside `ON`, the left side is preserved:

```sql
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
 AND s.country = 'Turkey'       -- 12 rows
```

**The exception:** to find non-matching rows you write
`WHERE right.column IS NULL` on purpose.

### 2. Rows multiplying

`orders` has ten rows and `order_items` twenty. Join them and the result
is **twenty** rows: each order's details repeat once per line.

The concrete consequences:

- `COUNT(*)` no longer gives the number of orders → use
  `COUNT(DISTINCT o.id)`
- `SUM(o.some_column)` adds the same value several times

The second is the dangerous one: something that should be counted once per
order gets counted once per line and the total inflates. No error, just a
wrong figure.

### 3. COUNT(*) after a LEFT JOIN

```sql
SELECT c.name, COUNT(*) FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.name;
```

For a customer with no orders the result is **1**, not 0. The `LEFT JOIN`
produces a row with empty columns for them, and `COUNT(*)` counts rows.

The correct form counts a column from the right table: `COUNT(o.id)` gives
**0** there.

### 4. A JOIN with no ON

```sql
FROM products p, categories c        -- old syntax, no ON
```

This pairs every product with every category: 12 × 4 = **48** rows. It is
called a Cartesian product.

Modern syntax uses `JOIN ... ON`, and leaving out the `ON` is an error.
The old comma syntax produces a Cartesian product silently — which is why
it is no longer used.

If you want one deliberately, it has a name: `CROSS JOIN`.

---

## A habit for checking

When you write a `JOIN`, look at three things:

1. **Is the row count what you expected?** Fewer than the left table means
   an `INNER JOIN` dropped rows; more means multiplication.
2. **Can you follow one row by hand?** Picking an order number and
   checking the result by eye saves fifteen minutes of searching.
3. **If you wrote `LEFT JOIN`, where is the condition on the right
   table?** If it is in `WHERE`, it probably belonged in `ON`.
