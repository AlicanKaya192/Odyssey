# Calculated Columns

So far you have returned columns that **sit** in the table. In this section
you will produce columns that do not exist: multiplying two of them,
shortening text, rounding a number.

`SELECT` does not only choose columns — you can write an **expression**
too.

## Arithmetic

```sql
SELECT name, price, stock, price * stock AS stock_value
FROM products;
```

There is no `price * stock` column in the table; it is computed while the
result is produced. Nothing is written to the table.

You get the four operations plus remainder: `+`, `-`, `*`, `/`, `%`.
Precedence works as in mathematics: `2 + 3 * 4` is **14**.

### The trap: integer division

This is where people new to SQL fall most often.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Not what you expect</h4>
      <pre><code>SELECT 7 / 2;
-- result: 3</code></pre>
    </div>
    <div class="ok">
      <h4>What you expect</h4>
      <pre><code>SELECT 7.0 / 2;
-- result: 3.5</code></pre>
    </div>
  </div>
  <figcaption>Divide two integers and the result is an integer, with the fractional part thrown away. Not rounded, truncated: 3, not 3.5.</figcaption>
</figure>

The same applies to columns: if `stock` is an `INT`, then `stock / 2` is an
integer. For a fractional result you have to make one side fractional:

```sql
SELECT stock / 2.0 AS yari
SELECT CAST(stock AS DECIMAL(10,2)) / 2 AS yari
```

The query raises no error and quietly gives the wrong number. When a
percentage in a report does not add up, this is the first place to look.

### NULL is contagious

```sql
SELECT 5 + NULL;   -- NULL
```

Any arithmetic containing `NULL` produces `NULL`. Write `price + kargo`
and if the shipping cost is empty the total is empty too.

The fix is to give the gap a value: `price + ISNULL(kargo, 0)`.

## Text functions

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">LEN(text)</span><span class="anat-body">Number of characters. <b>It does not count trailing spaces</b> — see below.</span></div>
    <div class="anat-row"><span class="anat-label">UPPER / LOWER</span><span class="anat-body">Converts to upper or lower case.</span></div>
    <div class="anat-row"><span class="anat-label">TRIM(text)</span><span class="anat-body">Removes leading and trailing spaces. For one side only, <code>LTRIM</code> / <code>RTRIM</code>.</span></div>
    <div class="anat-row"><span class="anat-label">LEFT(text, n)</span><span class="anat-body">The first n characters. For the end, <code>RIGHT</code>.</span></div>
    <div class="anat-row"><span class="anat-label">SUBSTRING(text, start, length)</span><span class="anat-body">Takes a piece from the middle. <b>Counting starts at 1</b>, not 0.</span></div>
    <div class="anat-row"><span class="anat-label">REPLACE(text, old, new)</span><span class="anat-body">Replaces every occurrence.</span></div>
  </div>
</figure>

### The trap: LEN does not count trailing spaces

```sql
SELECT LEN('abc   ');         -- 3
SELECT DATALENGTH('abc   ');  -- 6
SELECT LEN('   abc');         -- 6
```

`LEN` ignores **trailing** spaces but counts **leading** ones. The
asymmetry is surprising.

For the real length there is `DATALENGTH`, but that counts bytes rather
than characters — two bytes per character on `NVARCHAR` columns.

## Joining text: CONCAT, not +

There are two ways and they **do not do the same thing**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">'a' + NULL</span><span class="anat-body"><b>NULL</b> — one empty piece wipes out the whole result</span></div>
    <div class="anat-row"><span class="anat-label">CONCAT('a', NULL, 'b')</span><span class="anat-body"><b>'ab'</b> — it skips the empty piece</span></div>
    <div class="anat-row"><span class="anat-label">'a' + 1</span><span class="anat-body"><b>an error</b> — it tries to turn the text into a number</span></div>
    <div class="anat-row"><span class="anat-label">CONCAT('a', 1)</span><span class="anat-body"><b>'a1'</b> — it converts the number itself</span></div>
  </div>
  <figcaption>A query joining a first and last name with `+` produces a completely empty cell for people with no surname recorded. CONCAT does not.</figcaption>
</figure>

The rule is simple: **use `CONCAT` when joining text.** `+` is only safe
when you are certain both sides are text and neither is empty.

## Numeric functions

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ROUND(number, digits)</span><span class="anat-body">Rounds. <code>ROUND(2.5, 0)</code> → 3, <code>ROUND(2.345, 2)</code> → 2.35</span></div>
    <div class="anat-row"><span class="anat-label">CEILING / FLOOR</span><span class="anat-body">Up or down to a whole number. <code>CEILING(2.1)</code> → 3, <code>FLOOR(2.9)</code> → 2</span></div>
    <div class="anat-row"><span class="anat-label">ABS(number)</span><span class="anat-body">Absolute value.</span></div>
  </div>
</figure>

`ROUND` rounds halves **away from zero**: 2.5 → 3 and 3.5 → 4. Python's
`round` does not (it rounds to even, so `round(2.5)` is 2); this is why the
same calculation can differ between the two languages.

## Converting types: CAST and TRY_CAST

```sql
SELECT CAST(price AS INT) FROM products;
```

On a value that cannot be converted, `CAST` **raises an error** and the
whole query fails:

```sql
SELECT CAST('abc' AS INT);      -- Conversion failed
SELECT TRY_CAST('abc' AS INT);  -- NULL
```

`TRY_CAST` gives `NULL` when it cannot convert, and the query carries on.
When you are not sure the data is clean, `TRY_CAST` is safer — especially
on text columns that came from users.

## A calculated column inside WHERE

In the previous sections we said an alias cannot be used in `WHERE`. But
**the expression itself can be**:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Does not work</h4>
      <pre><code>SELECT price * stock AS deger
FROM products
WHERE deger &gt; 100000;</code></pre>
    </div>
    <div class="ok">
      <h4>Works</h4>
      <pre><code>SELECT price * stock AS deger
FROM products
WHERE price * stock &gt; 100000;</code></pre>
    </div>
  </div>
  <figcaption>Same reason as before: WHERE runs before SELECT. The alias does not exist yet, but the columns do — so you can write the calculation again there.</figcaption>
</figure>

Since `ORDER BY` runs last you can use the alias there and do not have to
repeat yourself.

### A note on speed

Wrapping a column in a **function** inside `WHERE` stops an index from
being used:

```sql
WHERE YEAR(tarih) = 2026        -- no index
WHERE tarih >= '2026-01-01'
  AND tarih <  '2027-01-01'     -- index usable
```

Both return the same rows, but the second is far faster on large tables.
Same reason as the `LIKE '%x'` problem: the server cannot tell where to
start.

## Summary

- You can write expressions inside `SELECT`; nothing is written to the
  table.
- **Dividing two integers gives an integer**: `7/2` is 3. For a fraction,
  make one side fractional.
- `NULL` is contagious in arithmetic; fill the gap with `ISNULL`.
- `LEN` does not count **trailing** spaces but does count leading ones.
- Use `CONCAT` to join text: it skips `NULL` and converts numbers itself.
- `ROUND` rounds halves away from zero (2.5 → 3).
- On data you do not trust, use `TRY_CAST` rather than `CAST`.
- An **alias** cannot be used inside `WHERE`, but an **expression** can.
