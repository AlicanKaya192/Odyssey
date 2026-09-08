A one-page summary of ordering, limiting and deduplicating.

## The order they are written in

```sql
SELECT   [DISTINCT] [TOP n] columns
FROM     table
WHERE    condition
ORDER BY column [ASC|DESC];
```

This order is **fixed**. Writing `WHERE` after `ORDER BY` is a syntax
error.

## ORDER BY

| Written as | What it does |
|---|---|
| `ORDER BY fiyat` | ascending (the default) |
| `ORDER BY fiyat ASC` | the same, written out |
| `ORDER BY fiyat DESC` | descending |
| `ORDER BY kategori, fiyat DESC` | category ascending, ties broken by price descending |
| `ORDER BY 2` | the second column of the `SELECT` list — **do not use** |

`DESC` applies **only to the column it is written on**. To reverse two
columns you have to write it on both.

## TOP

| Written as | What it does |
|---|---|
| `SELECT TOP 3 ...` | the first three rows |
| `SELECT TOP 10 PERCENT ...` | a tenth of the rows |
| `SELECT TOP 3 WITH TIES ...` | rows tied with the third come too |

`WITH TIES` only works when there is an `ORDER BY`, and it can make the
result longer than three rows.

**`TOP` is meaningless without `ORDER BY`.** If the order is undefined,
"the first three" is undefined too.

Other databases do this with `LIMIT` (`SELECT ... LIMIT 3`). SQL Server's
`TOP` comes right after `SELECT`, while `LIMIT` goes at the end of the
query.

## DISTINCT

It looks at the **whole selected row**, not at a single column.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Returns three rows</span><span class="anat-body"><code>SELECT DISTINCT kategori FROM urunler</code> — only the category is selected, so the repeats are removed.</span></div>
    <div class="anat-row"><span class="anat-label">Returns eight rows</span><span class="anat-body"><code>SELECT DISTINCT kategori, ad FROM urunler</code> — every <code>ad</code> differs, so every pair is unique.</span></div>
  </div>
</figure>

## The server's processing order

```
FROM -> WHERE -> SELECT -> ORDER BY
```

This has two concrete consequences:

- **`WHERE` cannot see an alias.** `SELECT fiyat AS tutar ... WHERE tutar > 1000`
  raises an error.
- **`ORDER BY` can see an alias.** In the same query,
  `ORDER BY tutar DESC` works.

## Where do NULLs land?

SQL Server treats `NULL` as the smallest value:

| Ordering | Where NULL goes |
|---|---|
| `ASC` | first |
| `DESC` | last |

This differs between databases. If the sorted column can hold `NULL`,
check where it lands.
