# Ordering and Limiting

In the previous section you learned to say which columns and which rows you
want. The result came back, but **its order was not yours to decide**.

This section covers three things: ordering the result (`ORDER BY`), taking
the first few rows (`TOP`) and removing duplicates (`DISTINCT`).

We continue with the same `products` table.

## The server guarantees no order

Let us settle this first, because most of the mistakes start here.

In a query with no `ORDER BY`, the order the rows come back in is
**undefined**. Today they may arrive in `id` order; tomorrow, once the
table has grown, in some other order. The server reads by whatever path it
finds fastest, and that path can change.

So: **if the order matters, you have to write `ORDER BY`.** Queries left
alone because "they come back sorted anyway" are the most common cause of
reports that break months later for no apparent reason.

## ORDER BY

You name the column to sort on:

```sql
SELECT name, price FROM products ORDER BY price;
```

The default is **ascending** (smallest first). Write `ASC` to say so
explicitly, or `DESC` for the reverse:

```sql
SELECT name, price FROM products ORDER BY price DESC;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ASC</span><span class="anat-body">ascending — smallest to largest, A to Z. <b>The default</b>, applied even when you do not write it.</span></div>
    <div class="anat-row"><span class="anat-label">DESC</span><span class="anat-body">descending — largest to smallest, Z to A.</span></div>
  </div>
</figure>

### Ordering on several columns

You add them with commas. **The order matters:** rows are sorted by the
first column, and rows that tie there are sorted among themselves by the
second:

```sql
SELECT category, name, price
FROM products
ORDER BY category, price DESC;
```

This puts the categories in alphabetical order and, inside each category,
sorts from expensive to cheap.

**Each column carries its own direction.** In
`ORDER BY category, price DESC` the `DESC` applies only to `price`;
`category` is still ascending. To reverse both you have to write it twice.

## ORDER BY runs last

In the previous section you saw that you cannot use an alias inside
`WHERE`. `ORDER BY` is the **opposite**:

<figure class="fig">
  <div class="flow">
    <span class="node">FROM</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE</span>
    <span class="arrow">-&gt;</span>
    <span class="node">SELECT</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">ORDER BY</span>
  </div>
  <figcaption>ORDER BY runs last, so the aliases SELECT produced are ready by then.</figcaption>
</figure>

```sql
SELECT name, price AS amount
FROM products
ORDER BY amount DESC;
```

This works. The same alias inside `WHERE` would have raised an error. One
rule, two different outcomes: **`WHERE` is early, `ORDER BY` is late.**

### Ordering by column number

You can write `ORDER BY 2` — meaning "the second column in the `SELECT`
list". It is short, but **do not use it**: the moment someone adds a column
to the `SELECT` list, the query quietly starts sorting on a different one.
Write the name.

## TOP: the first few rows

```sql
SELECT TOP 3 name, price
FROM products
ORDER BY price DESC;
```

The three most expensive products. `TOP` goes **right after `SELECT`**;
this is specific to T-SQL — other databases have `LIMIT`.

**Never write `TOP` without `ORDER BY`.** There is no such thing as "the
first 3": if the order is undefined, which three you get is undefined too.
The query raises no error and can return something different on every run.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Meaningless</h4>
      <pre><code>SELECT TOP 3 name
FROM products;</code></pre>
    </div>
    <div class="ok">
      <h4>Meaningful</h4>
      <pre><code>SELECT TOP 3 name
FROM products
ORDER BY price DESC;</code></pre>
    </div>
  </div>
  <figcaption>The one on the left means "three products at random". The one on the right means "the three most expensive products". Both run; only one answers a question.</figcaption>
</figure>

There are two extras:

- `TOP 10 PERCENT` — a tenth of the row count.
- `TOP 3 WITH TIES` — rows **tied with the third** come back as well. If
  there is a tie on the sorting value, the result can be more than three
  rows.

## DISTINCT: removing duplicates

```sql
SELECT DISTINCT category FROM products;
```

Eight products yield three categories: `Accessory`, `Computer`, `Display`.

**`DISTINCT` looks at the whole selected row, not at one column.** This is
the most misunderstood part:

```sql
SELECT DISTINCT category, name FROM products;
```

This does **not** return three rows. Because every `name` is different,
every `(category, name)` pair is unique — all eight rows come back.
`DISTINCT` filters rows, not a column.

It also helps when counting the distinct values of a column:

```sql
SELECT COUNT(DISTINCT category) FROM products;
```

Counting comes in the next section; keep this one in mind for then.

## Where do NULLs go?

When a column has no value (`NULL`), SQL Server treats it as the
**smallest**: it comes first in ascending order and last in descending.
This behaviour differs between databases — PostgreSQL does the opposite. If
there are `NULL`s in what you sort, check where they land.

## The order of the keywords

The order the keywords are written in is fixed:

```sql
SELECT   [DISTINCT] [TOP n] columns
FROM     table
WHERE    condition
ORDER BY column [ASC|DESC];
```

`ORDER BY` always comes last. Writing `WHERE` after `ORDER BY` is a syntax
error.

## Summary

- Without `ORDER BY` the order is **undefined**; "it came back sorted" is
  not a guarantee.
- The default is `ASC`; `DESC` applies only to the column it is written on.
- With several columns the order matters: the first one dominates.
- `ORDER BY` runs last, so it **can use an alias** — the thing `WHERE`
  cannot do.
- Ordering by column number (`ORDER BY 2`) is fragile; write the name.
- `TOP` is meaningless without `ORDER BY`.
- `DISTINCT` looks at the **whole selected row**, not at one column.
