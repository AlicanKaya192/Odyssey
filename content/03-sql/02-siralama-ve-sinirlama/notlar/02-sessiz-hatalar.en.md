The mistakes in this section are mostly **silent**: the query runs, a
result comes back, and it does not answer the question you asked. The
server cannot tell you that.

## "It came back sorted anyway"

This is the expensive one.

A query with no `ORDER BY` may come back in `id` order today. The server
reads the table by whatever path it finds fastest, and that path changes
as the table grows, when an index is added, or when the server version
changes.

A report that looked right during development comes out shuffled in
production months later, and nobody can find what changed. What changed is
not the query — it is the server's choice.

**If the order matters, write it.** And if it does not, writing it costs
nothing.

## `TOP` with no `ORDER BY`

```sql
SELECT TOP 5 ad FROM urunler;
```

This returns "five products" but **which five** is undefined. If you meant
"the five most expensive" or "the five newest", you have to write the
ordering.

It raises no error and produces a result — which is exactly why it slips
through.

## `DESC` applied to only one column

```sql
ORDER BY kategori, fiyat DESC
```

That `DESC` is for **`fiyat` only**. `kategori` is still ascending. To
reverse both:

```sql
ORDER BY kategori DESC, fiyat DESC
```

This is the first place to look when the result order seems slightly off.

## `DISTINCT` removed less than expected

```sql
SELECT DISTINCT kategori, ad FROM urunler;
```

This gets written meaning "let me deduplicate the categories", but all
eight rows come back — because `DISTINCT` looks at the **whole row** and
every `ad` is different.

If you want the distinct values of one column, select only that column.

## An alias inside `WHERE`

```sql
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
```

This **raises an error** — `Invalid column name 'tutar'`. The server runs
`WHERE` before `SELECT`, and at that point the alias does not exist.

The same alias works inside `ORDER BY`, because that runs last.

Seeing the two side by side is useful: the same name, the same query,
working in one place and not the other. One cause: **the processing
order**.

## A habit for checking

With a sorted query, look at three things:

1. **How many rows came back?** Is it the number you expected?
2. **Is the first row right?** If you asked for the most expensive, is it
   really the most expensive?
3. **Is the last row right?** This is the fastest way to see the direction
   of the sort.

If all three hold, the ordering is almost certainly correct.
