`NULL` is what sets SQL apart from other languages. This note gathers
everything about it in one place; there is more here than this section
needs, but you will come back to it.

## What NULL is and is not

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NULL</span><span class="anat-body"><b>The value is unknown.</b> There is nothing in the cell.</span></div>
    <div class="anat-row"><span class="anat-label">0</span><span class="anat-body">A number. A known value that happens to be zero.</span></div>
    <div class="anat-row"><span class="anat-label">''</span><span class="anat-body">An empty string. A known value whose length happens to be zero.</span></div>
  </div>
  <figcaption>Three different things. A product with stock 0 is "out of stock"; one with NULL is "the stock has not been recorded".</figcaption>
</figure>

## Three-valued logic

A condition in SQL has three possible outcomes: **true**, **false** and
**unknown**.

`WHERE` keeps only the rows that are **true**. "Unknown" is discarded just
like "false" — which is why rows carrying `NULL` quietly disappear.

| Expression | Result |
|---|---|
| `NULL = NULL` | unknown |
| `NULL <> NULL` | unknown |
| `NULL = 5` | unknown |
| `NULL > 5` | unknown |
| `NULL + 5` | `NULL` |
| `NULL IS NULL` | **true** |
| `NULL IS NOT NULL` | false |

The last two matter: `IS NULL` is not a comparison but a **question about
state**. Its answer is always true or false.

## How do `AND` and `OR` behave with unknown?

| Expression | Result | Why |
|---|---|---|
| `unknown AND false` | **false** | if one is false the result is false |
| `unknown AND true` | unknown | |
| `unknown OR true` | **true** | if one is true the result is true |
| `unknown OR false` | unknown | |
| `NOT unknown` | unknown | the negation of unknown is unknown |

That last row is the source of the `NOT IN` trap.

## The `NOT IN` trap

```sql
WHERE code NOT IN ('A', 'B', NULL)
```

**No rows come back.** The reason:

```
code <> 'A' AND code <> 'B' AND code <> NULL
                              ^^^^^^^^^^^^ always unknown
```

In an `AND` chain, if one part is unknown and the others are true, the
result is "unknown"; it can never be "true".

The positive form, `IN`, does not have this problem: it is an `OR` chain
and one true part is enough.

**Defences:** add `IS NOT NULL` to the query producing the list, or use
`NOT EXISTS`.

### The second face of the same trap

Even when there is no `NULL` in the `NOT IN` list, **rows where the column
itself is `NULL` are dropped.**

There are twelve products; three have `supplier_code` `T1` and three have
`NULL`. Even so:

```sql
WHERE supplier_code NOT IN ('T1')   -- 6 rows, not 9
```

You expect nine (12 − 3) and get six. The three missing rows are the
`NULL` ones: the comparison `NULL <> 'T1'` is "unknown", and `WHERE`
discards them.

The same applies to `<>`: `WHERE supplier_code <> 'T1'` also gives six
rows.

If you want them all you have to say so:

```sql
WHERE (supplier_code <> 'T1' OR supplier_code IS NULL)
```

This is the question to ask every time you write a "negative" condition:
**can this column be `NULL`?** If it can, you have to decide what should
happen to those rows.

## Replacing NULL with a value

| Function | What it does |
|---|---|
| `ISNULL(column, 'none')` | gives the second value when the first is `NULL` |
| `COALESCE(a, b, c)` | gives the first one that is not `NULL` |
| `NULLIF(a, b)` | `NULL` when a equals b, otherwise a |

`COALESCE` is standard SQL, `ISNULL` is specific to SQL Server. When you
need more than two options `COALESCE` is the only way.

## NULL and ordering

SQL Server treats `NULL` as the **smallest** value: first with `ASC`, last
with `DESC`. PostgreSQL does the opposite.

## What is coming later

- **Aggregate functions skip `NULL`s.** `AVG(price)` ignores empty cells;
  `COUNT(*)` counts every row while `COUNT(column)` counts only the
  non-empty ones.
- **`JOIN` produces `NULL`s.** A `LEFT JOIN` fills the right table's
  columns with `NULL` for rows it could not match.
- **A `UNIQUE` constraint allows `NULL`** (one of them on SQL Server),
  because whether two unknown values are equal is itself unknown.
