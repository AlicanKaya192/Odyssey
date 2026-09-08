# Grouping

So far you have always returned **rows**: twelve products, six products,
three products. In this section you will **summarise** them: how many
products there are, what the average price is, how many are in each
category.

There are two new pieces: **functions** that collapse rows, and
**`GROUP BY`**, which splits them into groups.

## Aggregate functions

They look at every row of a column and produce **a single number**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body">The number of rows.</span></div>
    <div class="anat-row"><span class="anat-label">SUM(column)</span><span class="anat-body">The total.</span></div>
    <div class="anat-row"><span class="anat-label">AVG(column)</span><span class="anat-body">The average.</span></div>
    <div class="anat-row"><span class="anat-label">MIN / MAX</span><span class="anat-body">The smallest / the largest.</span></div>
  </div>
</figure>

```sql
SELECT COUNT(*), MIN(price), MAX(price) FROM products;
```

The result is **one row**: 12, 95.00, 24500.00.

### The three forms of COUNT

These ask three different questions and give three different numbers:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body"><b>12</b> — the number of rows in the table. It does not look at columns at all.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(supplier_code)</span><span class="anat-body"><b>9</b> — the rows where that column is <b>filled</b>. <code>NULL</code> is not counted.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(DISTINCT category)</span><span class="anat-body"><b>4</b> — the number of different values in the column.</span></div>
  </div>
  <figcaption>The difference is not an accident, it is information: 12 minus 9 means three rows have no supplier recorded. It is the fastest way to see how much data is missing from a column.</figcaption>
</figure>

### Aggregate functions skip NULL

`AVG(price)` does **not** take empty cells into account — neither in the
numerator nor the denominator.

Most of the time that is what you want, but not always: when working out
an "average shipping cost", leaving out the orders with no cost recorded
pulls the average up. If you want an empty cell to count as zero, you have
to say so:

```sql
AVG(ISNULL(shipping, 0))
```

The decision is yours; the server does not make it for you, it quietly
skips.

### On an empty result, COUNT and SUM behave differently

```sql
SELECT COUNT(*)  FROM products WHERE price > 999999;   -- 0
SELECT SUM(price) FROM products WHERE price > 999999;  -- NULL
```

With no rows at all, `COUNT` says **zero** but `SUM` says **NULL** —
meaning "there was nothing to add up".

This distinction leaves blank cells in reports. If you want to see a zero,
write `ISNULL(SUM(price), 0)`.

### The integer trap inside AVG

The rule from the fourth section applies here too:

```sql
SELECT AVG(stock) FROM products;                         -- 27
SELECT AVG(CAST(stock AS DECIMAL(10,2))) FROM products;  -- 27.41
```

`stock` is an `INT` column, so `AVG` produces an integer and throws the
fraction away. No error, just the wrong average.

## GROUP BY: splitting into groups

```sql
SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category;
```

Four rows come back — one per category:

```
category    item_count
----------  ----------
Accessory   6
Computer    2
Display     2
Software    2
```

`GROUP BY` divides the rows into sets, and the aggregate functions now run
**separately for each set**.

### The most common mistake

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Raises an error</h4>
      <pre><code>SELECT category, name, COUNT(*)
FROM products
GROUP BY category;</code></pre>
    </div>
    <div class="ok">
      <h4>Correct</h4>
      <pre><code>SELECT category, COUNT(*)
FROM products
GROUP BY category;</code></pre>
    </div>
  </div>
  <figcaption>The Accessory group holds six products; the server cannot tell whose name it should print. The error message says exactly that: "Column products.name is invalid in the select list".</figcaption>
</figure>

The rule is one sentence: **every column in `SELECT` must either be in the
`GROUP BY` list or inside an aggregate function.**

If you want to see the name as well, you have to decide which one: the
most expensive (`MAX`), the alphabetically first (`MIN`), or all of them
(`STRING_AGG`)?

### NULL forms a group of its own

```sql
SELECT supplier_code, COUNT(*) FROM products GROUP BY supplier_code;
```

Four rows come back: `S1`, `S2`, `S3` and one for **NULL**.

Even though `NULL = NULL` is "unknown" in a comparison, in grouping two
empty values land in the **same** group. It looks inconsistent but it is
practical: otherwise every empty cell would be a group of its own.

### Grouping on several columns

```sql
SELECT category, supplier_code, COUNT(*)
FROM products
GROUP BY category, supplier_code;
```

Now a group is every distinct pair the two columns form **together**. The
result is nine rows — more than the number of categories and more than the
number of suppliers.

## HAVING: filtering groups

You want "the categories with more than two products". `WHERE` cannot do
it:

```sql
WHERE COUNT(*) > 2
-- error: An aggregate may not appear in the WHERE clause
```

Because `WHERE` runs **before the groups exist**; at that point there is
nothing to count.

The piece that filters groups is `HAVING`:

```sql
SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category
HAVING COUNT(*) > 2;
```

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>WHERE</h4>
      <p>Runs <b>before</b> grouping and removes individual <b>rows</b>.</p>
    </div>
    <div class="ok">
      <h4>HAVING</h4>
      <p>Runs <b>after</b> grouping and removes <b>groups</b>.</p>
    </div>
  </div>
  <figcaption>They can be used together: first throw away the rows you do not care about, then group what is left, then drop the small groups.</figcaption>
</figure>

```sql
SELECT category, COUNT(*) AS item_count
FROM products
WHERE stock > 0
GROUP BY category
HAVING COUNT(*) >= 2;
```

This query first drops the out-of-stock products, then groups by category
and returns the categories that still have at least two products.

## The new processing order

<figure class="fig">
  <div class="flow">
    <span class="node">FROM</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE<br>rows</span>
    <span class="arrow">-&gt;</span>
    <span class="node">GROUP BY</span>
    <span class="arrow">-&gt;</span>
    <span class="node">HAVING<br>groups</span>
    <span class="arrow">-&gt;</span>
    <span class="node">SELECT</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">ORDER BY</span>
  </div>
</figure>

This order explains three things at once:

- **No aggregate can appear in `WHERE`** — the groups do not exist yet.
- **No alias can be used in `HAVING`** — `SELECT` has not run. Write
  `HAVING item_count > 2` and you get "Invalid column name"; it has to be
  `HAVING COUNT(*) > 2`.
- **An alias can be used in `ORDER BY`** — that runs last.

```sql
SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category
HAVING COUNT(*) > 1        -- no alias here
ORDER BY item_count DESC;  -- alias is fine here
```

## Summary

- Aggregate functions collapse rows into a single value: `COUNT`, `SUM`,
  `AVG`, `MIN`, `MAX`.
- `COUNT(*)` counts rows, `COUNT(column)` counts the **filled** ones,
  `COUNT(DISTINCT column)` counts the **different** values.
- Aggregates skip empty values; with no rows at all `COUNT` gives zero
  while `SUM` gives an empty result.
- `AVG` on an integer column produces an integer — you need `CAST`.
- `GROUP BY` divides rows into sets; every column in `SELECT` must be in
  the grouping list or inside a function.
- In grouping, all empty values form **one single group**.
- `WHERE` removes rows **before** grouping, `HAVING` removes groups
  **after**.
- `HAVING` cannot see an alias; `ORDER BY` can.
