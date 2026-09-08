# Writing a Query: SELECT and WHERE

In the previous section you wrote `SELECT * FROM sehirler` and the whole
table came back. That is not what you want in real work: out of a table
with millions of rows you want **a few columns** and **a few rows**.

This section answers those two questions: which columns, which rows.

## The anatomy of a query

Every `SELECT` query is built from the same three parts:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body"><b>Which columns?</b> Comma-separated column names, or <code>*</code> for all of them.</span></div>
    <div class="anat-row"><span class="anat-label">FROM</span><span class="anat-body"><b>Which table?</b> Where the data comes from.</span></div>
    <div class="anat-row"><span class="anat-label">WHERE</span><span class="anat-body"><b>Which rows?</b> Optional. Leave it out and every row comes back.</span></div>
  </div>
  <figcaption>The order is fixed: SELECT, then FROM, then WHERE. They cannot be swapped.</figcaption>
</figure>

In this section you will work with a table called `urunler` ("products"):

| id | ad | kategori | fiyat | stok |
|---|---|---|---|---|
| 1 | Klavye | Aksesuar | 450.00 | 32 |
| 2 | Monitor | Ekran | 3200.00 | 8 |
| 3 | Fare | Aksesuar | 220.00 | 0 |

The columns are name, category, price and stock.

## Choosing columns

The star brings everything:

```sql
SELECT * FROM urunler;
```

Write the columns you want and only those come back:

```sql
SELECT ad, fiyat FROM urunler;
```

**The order is the order you wrote.** In the table `fiyat` comes after
`ad`, but if you want the other way round you write the other way round:

```sql
SELECT fiyat, ad FROM urunler;
```

### Why do we avoid the star?

It is handy while exploring, but in real work it has three problems:

- **It carries data you do not need.** Reading forty columns when two of
  them matter wears out the server and the network for nothing.
- **Your query changes when the table changes.** If someone adds a column,
  one day your query starts returning an extra one.
- **It hides your intent.** Somebody reading a `SELECT *` cannot see what
  you actually needed.

The rule: **star while exploring, column names in the query you keep.**

## Giving a column another name: AS

You can change the column heading in the result:

```sql
SELECT ad AS urun_adi, fiyat AS tutar FROM urunler;
```

Same data, different headings. This matters in a report, or in a result
some program is going to read.

You can leave `AS` out (`ad urun_adi`) but **write it anyway**: in a query
written without `AS`, a single forgotten comma silently turns two columns
into one.

## Choosing rows: WHERE

`WHERE` takes a **condition** and only the rows that satisfy it come back:

```sql
SELECT ad, fiyat FROM urunler WHERE kategori = 'Aksesuar';
```

The comparisons you can use in a condition:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">=</span><span class="anat-body">equal. <b>One equals sign</b> — there is no <code>==</code> in SQL.</span></div>
    <div class="anat-row"><span class="anat-label">&lt;&gt;</span><span class="anat-body">not equal. <code>!=</code> works too, but <code>&lt;&gt;</code> is the standard one.</span></div>
    <div class="anat-row"><span class="anat-label">&lt; &gt;</span><span class="anat-body">less than, greater than</span></div>
    <div class="anat-row"><span class="anat-label">&lt;= &gt;=</span><span class="anat-body">less or equal, greater or equal</span></div>
  </div>
</figure>

## Text goes in single quotes

In SQL, text is written inside **single quotes**:

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h4>Correct</h4>
      <pre><code>WHERE kategori = 'Ekran'</code></pre>
    </div>
    <div class="no">
      <h4>Raises an error</h4>
      <pre><code>WHERE kategori = "Ekran"</code></pre>
    </div>
  </div>
  <figcaption>In SQL Server a double quote does not mean text, it means an <b>object name</b>. Write "Ekran" and the server goes looking for a column called Ekran and does not find one.</figcaption>
</figure>

Numbers take no quotes: `WHERE fiyat > 1000`.

If the text itself contains a single quote, you write it twice:
`WHERE ad = 'Kadin''s'`. It is rarely needed, but when it is and you do
not know it, it burns hours.

### Upper and lower case

On a default installation SQL Server **does not distinguish case**:
`'aksesuar'` and `'Aksesuar'` count as the same. This depends on the
server's collation setting and can be changed — so do not assume it is
true on every server.

## Several conditions: AND, OR, NOT

```sql
SELECT ad FROM urunler
WHERE kategori = 'Aksesuar' AND fiyat < 300;
```

`AND` wants both, `OR` wants at least one. `NOT` inverts a condition.

**`AND` runs before `OR`.** This is like multiplication coming before
addition, and it is a trap in the same way:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Not what you meant</h4>
      <pre><code>WHERE kategori = 'Ekran'
   OR kategori = 'Aksesuar'
  AND fiyat &lt; 300</code></pre>
    </div>
    <div class="ok">
      <h4>If this is your intent</h4>
      <pre><code>WHERE (kategori = 'Ekran'
    OR kategori = 'Aksesuar')
  AND fiyat &lt; 300</code></pre>
    </div>
  </div>
  <figcaption>The query on the left says "every screen, plus accessories under 300". Without parentheses AND only binds the two conditions next to it.</figcaption>
</figure>

The rule is simple: **if you use both, add parentheses.** Even when it
would work anyway, the reader can see what you meant.

## The server does not run it in the order you wrote it

You write the query as `SELECT ... FROM ... WHERE ...`, but the server
processes it in this order:

<figure class="fig">
  <div class="flow">
    <span class="node">FROM<br>take the table</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE<br>sift the rows</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">SELECT<br>pick the columns</span>
  </div>
</figure>

This looks like trivia but it has a concrete consequence: **you cannot use
an alias from `SELECT` inside `WHERE`.**

```sql
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
```

This query says "there is no column called tutar". When `WHERE` runs,
`SELECT` has not run yet, so nothing called `tutar` exists. The correct
form:

```sql
SELECT fiyat AS tutar FROM urunler WHERE fiyat > 1000;
```

## The semicolon

The `;` at the end of a query is not required in SQL Server, but **make a
habit of it**: it is what separates several queries, and some statements
(like the `WITH` you will meet later) require the query before them to end
with one.

## Summary

- `SELECT` picks columns, `FROM` picks the table, `WHERE` picks rows.
- Star while exploring, column names in the query you keep.
- `AS` renames the heading in the result; do not skip writing it.
- Text goes in **single quotes**; a double quote means an object name.
- Equality is a single `=`; there is no `==`.
- `AND` runs before `OR` — if you use both, add parentheses.
- The server runs `FROM → WHERE → SELECT`, which is why an alias cannot be
  used in `WHERE`.
