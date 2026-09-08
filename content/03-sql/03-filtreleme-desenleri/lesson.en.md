# Filtering Patterns

You know how to compare one value at a time with `WHERE`. This section
gives you four more tools: searching for a **pattern** inside text,
choosing from a **list**, giving a **range**, and finding rows with **no
value**.

The last one — `NULL` — is not just a tool; it is a behaviour that sets SQL
apart from other languages. Half the section is about it.

The `urunler` table has grown a little here: it now has a `tedarikci_kod`
column ("supplier code"), and **for some products that column is empty.**

## LIKE: a text pattern

Instead of exact equality you want "starts with" or "contains":

```sql
SELECT ad FROM urunler WHERE ad LIKE 'K%';
```

There are two wildcards:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">%</span><span class="anat-body"><b>Zero or more</b> characters. <code>'K%'</code> is everything starting with K, <code>'%uk'</code> everything ending in uk, <code>'%la%'</code> everything containing la.</span></div>
    <div class="anat-row"><span class="anat-label">_</span><span class="anat-body"><b>Exactly one</b> character. <code>'F_re'</code> is four letters long, starting with F and ending in re.</span></div>
  </div>
</figure>

Case does not matter on a default installation: `'k%'` and `'K%'` give the
same result.

### Searching for the wildcard itself

If you really are looking for a `%` sign inside the text, you define an
escape character with `ESCAPE`:

```sql
WHERE aciklama LIKE '%50!%%' ESCAPE '!'
```

Here `!%` means a literal percent sign; the last `%` is still a wildcard.
It is rarely needed, but when it is there is no other way.

### `LIKE 'x%'` is not the same as `LIKE '%x'`

For performance these are very different. `'K%'` — a pattern with a
**known beginning** — can use an index. `'%K'` or `'%K%'` requires looking
at every row. On small tables you cannot tell; on tables with millions of
rows it is measured in seconds.

## IN: one of a list

Instead of long `OR` chains:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>The long form</h4>
      <pre><code>WHERE kategori = 'Ekran'
   OR kategori = 'Aksesuar'
   OR kategori = 'Yazilim'</code></pre>
    </div>
    <div class="ok">
      <h4>The short form</h4>
      <pre><code>WHERE kategori IN
  ('Ekran', 'Aksesuar', 'Yazilim')</code></pre>
    </div>
  </div>
  <figcaption>The two do exactly the same job. The one on the right is shorter and avoids the parenthesis trap: forgetting them while joining an OR chain to an AND is one of the most common mistakes.</figcaption>
</figure>

There is an opposite too: `NOT IN`. But **`NOT IN` together with `NULL` is
dangerous** — more on that shortly.

## BETWEEN: a range

```sql
SELECT ad, fiyat FROM urunler WHERE fiyat BETWEEN 500 AND 3000;
```

**Both ends are included.** This query means
`fiyat >= 500 AND fiyat <= 3000`. Rows priced at exactly 500 and exactly
3000 come back.

This is the detail people misremember most often. If "between 500 and
3000" is meant to exclude 3000, `BETWEEN` is the wrong tool:

```sql
WHERE fiyat >= 500 AND fiyat < 3000
```

The order matters too: `BETWEEN 3000 AND 500` returns **no rows at all**
and raises no error. The smaller value goes first.

## NULL: no value

Now for the real subject of the section.

`NULL` is **not an empty string and not zero.** It means "there is no value
in this cell" — more precisely, **"the value is unknown"**.

The difference is concrete: if a product's supplier is `NULL` we are not
saying "it has no supplier", we are saying "who its supplier is has not
been recorded".

### `= NULL` is never true

```sql
WHERE tedarikci_kod = NULL      -- always an empty result
```

This query raises no error and **returns no rows.** The reason: any
comparison made with an unknown value is itself unknown.

Logic in SQL is **three-valued**: true, false and **unknown**. `WHERE`
keeps only the rows that are **true**; "unknown" is discarded just like
"false".

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NULL = NULL</span><span class="anat-body">unknown — whether two unknown values are equal is also unknown</span></div>
    <div class="anat-row"><span class="anat-label">NULL &lt;&gt; 5</span><span class="anat-body">unknown</span></div>
    <div class="anat-row"><span class="anat-label">NULL &gt; 100</span><span class="anat-body">unknown</span></div>
    <div class="anat-row"><span class="anat-label">NULL IS NULL</span><span class="anat-body"><b>true</b> — this is the only thing that works</span></div>
  </div>
</figure>

### The right way: IS NULL

```sql
SELECT ad FROM urunler WHERE tedarikci_kod IS NULL;
SELECT ad FROM urunler WHERE tedarikci_kod IS NOT NULL;
```

`IS NULL` is not a comparison but a **question about state**: "is this cell
empty?" Its answer is always true or false.

### The silent trap: NOT IN and NULL

This is one of the most painful behaviours in SQL.

```sql
WHERE tedarikci_kod NOT IN ('T1', 'T2', NULL)
```

This query returns **no rows at all.** And raises no error.

The reason: `x NOT IN (a, b, c)` really means
`x <> a AND x <> b AND x <> c`. If the list contains `NULL`, one of those
comparisons is always "unknown", and the `AND` chain can never be "true".

When you write the list yourself you would not put `NULL` in it. But when
the list comes from **another query** (the subqueries you will meet later)
it can contain `NULL`, and the query quietly returns nothing.

There are two defences: add `WHERE ... IS NOT NULL` to the query producing
the list, or use `NOT EXISTS` instead of `NOT IN`. The second belongs to
the subqueries section.

## NULL and ordering

It came up in the previous section: SQL Server treats `NULL` as the
smallest value. It comes first in ascending order and last in descending.

## All of it together

```sql
SELECT ad, fiyat
FROM urunler
WHERE kategori IN ('Aksesuar', 'Ekran')
  AND fiyat BETWEEN 200 AND 2000
  AND tedarikci_kod IS NOT NULL
  AND ad LIKE '%a%'
ORDER BY fiyat DESC;
```

All four are joined with `AND` and all of them live inside the same
`WHERE`.

## Summary

- `LIKE` searches for a pattern: `%` is many characters, `_` is exactly
  one.
- If the pattern has a **known beginning** (`'K%'`) the query is fast;
  `'%K%'` looks at every row.
- `IN` is the short form of a long `OR` chain; `BETWEEN` is a range with
  **both ends included**.
- `BETWEEN` does not exclude its bounds; if you need that, write `>=` and
  `<`.
- `NULL` means "unknown"; it is not an empty string and not zero.
- `= NULL` is **never** true. Write `IS NULL` / `IS NOT NULL`.
- `NOT IN` against a list containing `NULL` **always** returns nothing.
