A one-page list of the aggregate functions. The numbers in the result
column were actually measured on this section's `products` table.

## The functions

| Function | What it does | Example result |
|---|---|---|
| `COUNT(*)` | counts rows | `12` |
| `COUNT(column)` | counts rows where the column is **filled** | `COUNT(supplier_code)` → `9` |
| `COUNT(DISTINCT column)` | counts **different** values | `COUNT(DISTINCT category)` → `4` |
| `SUM(column)` | adds up | `SUM(stock)` → `329` |
| `AVG(column)` | takes the average | `AVG(price)` → `5108.75` |
| `MIN` / `MAX` | smallest / largest | `95.00` / `24500.00` |

`MIN` and `MAX` work on text too: they give the alphabetically first and
last value.

## How they treat empty values

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">All of them skip</span><span class="anat-body"><code>SUM</code>, <code>AVG</code>, <code>MIN</code>, <code>MAX</code> and <code>COUNT(column)</code> leave empty cells out of the calculation.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(*) is the exception</span><span class="anat-body">It never looks at a column, so empty cells do not affect it.</span></div>
    <div class="anat-row"><span class="anat-label">Watch out with AVG</span><span class="anat-body">Empty cells drop out of the <b>denominator</b> as well. If three of ten orders have no shipping cost, the average is divided by seven, not ten.</span></div>
  </div>
</figure>

If you want an empty cell to count as zero, you say so:
`AVG(ISNULL(shipping, 0))`.

## When there are no rows at all

| Query | Result |
|---|---|
| `COUNT(*)` | `0` |
| `SUM(price)` | `NULL` |
| `AVG(price)` | `NULL` |
| `MIN` / `MAX` | `NULL` |
| with `GROUP BY` | **no rows at all** |

`COUNT` is the one exception: it can say "I counted zero rows". The others
say "there was nothing to add up".

If you want a zero in the report, write `ISNULL(SUM(price), 0)`.

## The integer trap is inside AVG too

```sql
SELECT AVG(stock) FROM products;                         -- 27
SELECT AVG(CAST(stock AS DECIMAL(10,2))) FROM products;  -- 27.41
```

`stock` is an `INT`, so both the total and the division are integers. The
fraction is thrown away and the query raises no error.

Get into the habit of checking the column's type when you take an average.

## The GROUP BY rule

**Every column in `SELECT` must either be in the `GROUP BY` list or inside
an aggregate function.**

```sql
-- does not work: the Accessory group has six names, which one?
SELECT category, name, COUNT(*) FROM products GROUP BY category;

-- works: you said which one you wanted
SELECT category, MAX(name), COUNT(*) FROM products GROUP BY category;
```

## The order, and what each part can see

```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY
```

| Part | Aggregate | Alias |
|---|---|---|
| `WHERE` | **no** | no |
| `HAVING` | yes | **no** |
| `ORDER BY` | yes | **yes** |

All three rows have the same cause: a part cannot see something that runs
**after** it.

## Common patterns

```sql
-- how many empty cells are in a column
SELECT COUNT(*) - COUNT(supplier_code) FROM products;

-- how many distinct values per group
SELECT category, COUNT(DISTINCT supplier_code)
FROM products GROUP BY category;

-- categories with only one product
SELECT category FROM products
GROUP BY category HAVING COUNT(*) = 1;

-- finding duplicate records
SELECT name, COUNT(*) FROM products
GROUP BY name HAVING COUNT(*) > 1;
```

The last one is the most frequently used grouping query in practice:
hunting for duplicates.
