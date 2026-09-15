# Indexes

Every query so far came back instantly, because the tables had ten rows.
This section adds a ninth table to the schema: `events`, with 20,000
rows — the customers' actions on the website. The question is: how does
the server find the row it is looking for, and why does it sometimes
fail to?

```
events: id, customer_id, product_id, event_type, session_code, created_at, amount
```

One event every 25 minutes, from January 1 to December 14, 2025: 58
events a day. Each of the four types (`view`, `click`, `cart`,
`purchase`) has 5,000 rows; `amount` is only filled in for purchases.

## How it is measured

The numbers in this section are **reads**: the number of 8 KB pages the
server looks at for a query. Time varies from machine to machine; reads
do not. Tell the server `SET STATISTICS IO ON` and after every query it
gives a message like this (measured):

```
Table 'events'. Scan count 1, logical reads 150, physical reads 0, ...
```

The data of the `events` table is 150 pages. The application's result
table does not show these messages; the measurements in this section were
made separately in SQL Server. If you use SQL Server Management Studio,
you can see them yourself with the same command.

## What an index is

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Clustered index</span><span class="anat-body">The table itself, sorted by the primary key. <code>PRIMARY KEY</code> builds it by itself — measured, on all nine tables.</span></div>
    <div class="anat-row"><span class="anat-label">Nonclustered index</span><span class="anat-body">A separate, sorted list: the values of the chosen column and a pointer from each to its row. The index at the back of a book.</span></div>
    <div class="anat-row"><span class="anat-label">Seek</span><span class="anat-body">Going straight to the right place in a sorted list.</span></div>
    <div class="anat-row"><span class="anat-label">Scan</span><span class="anat-body">Reading from start to end — the table or the index.</span></div>
    <div class="anat-row"><span class="anat-label">Key Lookup</span><span class="anat-body">Going back to the table for a column the index does not have. Once per row.</span></div>
  </div>
</figure>

A search by primary key, like `id = 10000`, is already fast: 2 reads, a
*Clustered Index Seek*. Because the table is kept in `id` order, the
server goes straight to that page.

## The first index

One day's events:

```sql
SELECT id, created_at FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

The table is in `id` order; there is no order by `created_at`. For 58
rows the server looks at all 150 pages. An index:

```sql
CREATE INDEX ix_events_created ON events (created_at);
```

<figure class="fig">
  <div class="versus">
    <div>
      <h4>No index</h4>
      <p><strong>150 reads</strong></p>
      <p>Clustered Index Scan: every page of the table.</p>
    </div>
    <div>
      <h4>created_at index</h4>
      <p><strong>2 reads</strong></p>
      <p>Index Seek: the place in the sorted list where June 1 begins.</p>
    </div>
  </div>
</figure>

The same 58 rows. The price is space: `sp_spaceused` showed the space
taken by indexes going from 16 KB to 352 KB.

## A function on the column: the index goes blind

The index is sorted by `created_at` values — not by `YEAR(created_at)`.
Once the column goes inside a function, the server cannot go straight to
the right place in the sorted list; it has to work out the function for
every value and look. Measured, with the index in place:

| `WHERE` | Reads | Plan |
|---|---|---|
| `created_at >= '2025-06-01' AND created_at < '2025-06-02'` | 2 | Index Seek |
| `YEAR(created_at) = 2025 AND MONTH(created_at) = 6 AND DAY(created_at) = 1` | 42 | Index Scan |
| `DATEADD(day, 1, created_at) >= '2025-06-02' AND ... < '2025-06-03'` | 42 | Index Scan |
| `CAST(created_at AS DATE) = '2025-06-01'` | 2 | Index Seek |

42 is the whole index: less than 150 because the index is smaller than
the table, but twenty times the 2 of a seek. `CAST(... AS DATE)` is an
exception — the server recognises that conversion and can still seek
(measured). Do not generalise from it: the rule is **leave the column
bare** and put the function on the other side.

The same goes for text (with an index on `session_code`):

| `WHERE` | Reads | Plan |
|---|---|---|
| `session_code = 'S010000'` | 2 | Index Seek |
| `session_code LIKE 'S0050%'` | 3 | Index Seek |
| `session_code LIKE '%0050'` | 54 | Index Scan |
| `UPPER(session_code) = 'S010000'` | 54 | Index Scan |

A `LIKE` with a known beginning can be sought in a sorted list; one that
starts with `%` cannot — you cannot look up "words ending in *-ing*" in
a book's index.

The half-open range of the tenth section now has a second reason.

## The index is there, but not used

With the `created_at` index in place:

| Query (June 1) | Rows | Reads | Plan |
|---|---|---|---|
| `SELECT id, created_at` | 58 | 2 | Index Seek |
| `SELECT *` | 58 | **150** | Clustered Index Scan |
| `SELECT created_at, amount` | 58 | **150** | Clustered Index Scan |
| purchases: `SELECT id, created_at, amount ... AND event_type = N'purchase'` | 15 | 130 | Index Seek + Key Lookup |

The index only holds `created_at` (and `id`, to find the row). When
another column is asked for, the server has to go back to the table for
every row. For 58 rows it judged 58 trips back as expensive as a scan
and **did not use the index at all**; for 15 rows it used the index and
went back for each (130 reads). The server makes the call: an index
existing does not mean it will be used.

The same happens with columns of low selectivity. `event_type` takes four
values; `'purchase'` is a quarter of the table (5,000 rows). With an
index on that column, `SELECT id` came from the index in 22 reads,
while `SELECT *` still scanned the table (150).

## A covering index: INCLUDE

If everything the query asks for is in the index, there is no need to go
back to the table:

```sql
CREATE INDEX ix_events_created ON events (created_at) INCLUDE (amount);
```

`SELECT created_at, amount` for one day: 150 with the `created_at` index
(a scan), **3** with `INCLUDE (amount)` (an Index Seek). The column in
`INCLUDE` does not take part in the sort order; it only sits in the
index. A two-column key `(created_at, amount)` also gave 3 reads for the
same query; the difference is that there `amount` is part of the sort
order.

## A composite index: the order matters

A phone book is sorted by surname, then first name. Knowing the surname,
you go to the right page; knowing only the first name, you read the whole
book. A two-column index is the same. Measured:

| Query | `(customer_id, created_at)` | `(created_at, customer_id)` |
|---|---|---|
| customer 3, one day | 2 — seek | 2 — seek |
| customer 3 only (3,334 rows) | 11 — seek | 52 — scan |
| one day only | 52 — scan | 2 — seek |

An index can go straight to the right place in searches where its
**first column** is known. When both columns were searched together,
either order was enough; the difference shows when searching with one
column. The habit: the column searched with equality (`customer_id = 3`)
first, the one searched with a range (`created_at >= ...`) second — so
the same customer's rows sit together, in date order.

## A filtered index

`amount` is empty on 15,000 of the 20,000 rows. An index can hold only
the filled-in ones:

```sql
CREATE INDEX ix_events_amount ON events (amount) WHERE amount IS NOT NULL;
```

| | Measured |
|---|---|
| `WHERE amount > 490` (120 rows) | 2 reads, Index Seek |
| `WHERE amount IS NULL` | 150 reads — those rows are not in the index |
| space taken by indexes, filtered | 128 KB |
| the same index without a filter | 408 KB |

## A unique index

A `UNIQUE` index accepts no duplicates — neither when it is created nor
afterwards (measured):

| Written as | Result |
|---|---|
| `CREATE UNIQUE INDEX ... ON customers (city)` | `The CREATE UNIQUE INDEX statement terminated because a duplicate key was found ... The duplicate key value is (Istanbul).` |
| `CREATE UNIQUE INDEX ... ON customers (name)` | created |
| adding a second customer with the same name | `Cannot insert duplicate key row in object 'dbo.customers' with unique index 'ux_customers_name'. The duplicate key value is (Nova Retail).` |

The `UNIQUE` rule of the ninth section builds the same thing behind the
scenes: after `ALTER TABLE customers ADD CONSTRAINT uq_customers_name
UNIQUE (name)`, `sys.indexes` showed a unique, nonclustered index. That
index cannot be removed with `DROP INDEX` — the rule is using it (`An
explicit DROP INDEX is not allowed ...`); you remove the rule itself.

## The price

Every index is updated **too** when a row is added, deleted or changed.
Adding a single row (measured):

| On the table | Reads |
|---|---|
| only the primary key | 2 |
| the primary key + five indexes | 22 |

And space. That is why indexes are built not "on every column" but for
**queries that really run often**.

## Seeing and removing indexes

```sql
SELECT name, type_desc
FROM sys.indexes
WHERE object_id = OBJECT_ID('events') AND type > 0;
```

After the `created_at` index two rows came back: the primary key's
`CLUSTERED` index and `ix_events_created` (`NONCLUSTERED`).

```sql
DROP INDEX ix_events_created ON events;
```

| Written as | Error |
|---|---|
| `DROP INDEX ix_events_created` (no table) | `Must specify the table name and index name for the DROP INDEX statement.` |
| dropping an index that does not exist | `Cannot drop the index 'events.ix_yok', because it does not exist ...` |
| a second index with the same name | `The operation failed because an index or statistics with name ... already exists on table ...` |

Because every run is rolled back at the end in this application, an index
you create in an exercise is not there on the next run (measured: an
index created inside a transaction was gone from `sys.indexes` after the
rollback).

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">CREATE INDEX</span><span class="anat-body">A sorted copy of the chosen columns; a search drops from 150 reads to 2.</span></div>
    <div class="anat-row"><span class="anat-label">Leave the column bare</span><span class="anat-body"><code>YEAR(column)</code>, <code>UPPER(column)</code>, <code>LIKE '%...'</code> push the index into a scan.</span></div>
    <div class="anat-row"><span class="anat-label">INCLUDE</span><span class="anat-body">Add the columns the query asks for to the index; no more trips back to the table.</span></div>
    <div class="anat-row"><span class="anat-label">Order</span><span class="anat-body">A composite index can be sought by its first column; equality first, range second.</span></div>
    <div class="anat-row"><span class="anat-label">Filter</span><span class="anat-body">With <code>WHERE</code>, only the rows needed; a smaller index.</span></div>
    <div class="anat-row"><span class="anat-label">Price</span><span class="anat-body">Every index slows down writes and takes space.</span></div>
  </div>
</figure>

The next section is views and stored procedures: binding a query you
write often to a name inside the database.
