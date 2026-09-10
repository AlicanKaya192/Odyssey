# Changing Data

For seven sections you only ever **read** the data. Whatever you wrote in
a `SELECT`, nothing in the table changed: a wrong query gave a wrong
answer, and that was all.

In this section you start writing. There are three commands — `INSERT`,
`UPDATE`, `DELETE` — and they share one property: **there is no undo
button.**

## First, know this: you are safe here

Everything you write in Odyssey is rolled back when the run finishes.
Even if you delete every table, they are all in place on your next
attempt.

A real database has no such net. That is exactly why the habits in this
section exist.

## INSERT: adding rows

```sql
INSERT INTO categories (code, name)
VALUES ('NET', 'Networking');
```

Three parts: **which table**, **which columns**, **which values**.

It also works without the column list:

```sql
INSERT INTO categories VALUES ('NET', 'Networking');
```

That runs, but **do not write it**. The values are handed out by the
table's column order; add a column to the table tomorrow and this
statement quietly starts writing to the wrong place. The `INSERT` with a
column list keeps working.

### Many rows at once

```sql
INSERT INTO categories (code, name) VALUES
    ('NET', 'Networking'),
    ('PRN', 'Printing');
```

Two rows go in and the server says "2 rows affected". Same result as two
separate `INSERT`s, but one command is faster and **either both go in or
neither does**.

### The values can come from a query

```sql
INSERT INTO categories (code, name)
SELECT ... FROM ...;
```

You write a `SELECT` in place of `VALUES`. The number and order of the
columns have to line up. This is the shortest way to move data from one
table to another.

### When it fails

There are three common cases; all three were measured:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Missing column</span><span class="anat-body"><code>Cannot insert the value NULL into column 'name' ... column does not allow nulls.</code> The column is <code>NOT NULL</code> and you gave no value.</span></div>
    <div class="anat-row"><span class="anat-label">Counts differ</span><span class="anat-body"><code>There are more columns in the INSERT statement than values specified in the VALUES clause.</code></span></div>
    <div class="anat-row"><span class="anat-label">Duplicate key</span><span class="anat-body"><code>Violation of PRIMARY KEY constraint ... The duplicate key value is (ACC).</code> That key is already there.</span></div>
  </div>
</figure>

These errors are **good news**: the server is protecting you from bad
data. The genuinely dangerous statements are the ones that raise no
error — they are coming next.

## UPDATE: changing what is there

```sql
UPDATE products
SET price = price * 1.10
WHERE category_code = 'ACC';
```

`SET` says what changes, `WHERE` says on which rows. This query updates
**six rows**.

On the right-hand side you can use the column itself: `price = price *
1.10` means "raise the price by 10%". The server reads each row's own old
value.

Several columns, separated by commas:

```sql
UPDATE products
SET price = 500.00, stock = 40
WHERE id = 1;
```

### If you forget the WHERE

```sql
UPDATE products SET price = price * 1.10;
```

This changes **all twelve of the twelve rows** (measured). No error, no
warning, no "are you sure". The server does exactly what you said —
because an `UPDATE` with no `WHERE` really does mean "all of them".

Every price in the catalogue went up 10% and you no longer know which
ones were right.

**An `UPDATE` with no `WHERE`, a `DELETE` with no `WHERE`, and `DROP
TABLE`** are the three classic disasters of database work.

## DELETE: removing rows

```sql
DELETE FROM orders
WHERE status = 'cancelled';
```

No `SELECT`, no columns: the whole row goes. This query deletes one row,
leaving nine orders.

And yes, the same trap is here too:

```sql
DELETE FROM shipments;
```

All six rows, gone.

### DELETE, TRUNCATE, DROP

The three get confused, though the differences are clear:

<figure class="fig">
  <div class="versus">
    <div>
      <h4>DELETE</h4>
      Removes rows. Can take a <code>WHERE</code>. Part of the transaction, so it can be rolled back. Tells you how many rows it removed.
    </div>
    <div>
      <h4>TRUNCATE</h4>
      Empties the <b>whole</b> table. Takes no <code>WHERE</code>. Much faster, but does not tell you how many rows went.
    </div>
    <div class="no">
      <h4>DROP</h4>
      <b>Destroys</b> the table. Not the rows — the table itself.
    </div>
  </div>
</figure>

`TRUNCATE` does not delete rows one by one, it resets the table — which
is why it is fast. If you need to empty a million-row table, that is the
right tool.

## How many rows were affected

All three commands tell you how many rows they touched when they finish.
Odyssey shows this in the result panel, and you can read it in your own
query too:

```sql
UPDATE products SET stock = stock + 1 WHERE category_code = 'ACC';
SELECT @@ROWCOUNT AS affected;
```

The result: **6**.

That number is your best check. If you say "I am updating one customer"
and see 40, something is wrong in the `WHERE` — and you see it **before**
the data is ruined.

## Before you write: rehearse with SELECT

The most important habit in this section is one line long:

```sql
-- run this first
SELECT * FROM products WHERE category_code = 'ACC';

-- once you see it brings back the right rows
UPDATE products SET price = price * 1.10 WHERE category_code = 'ACC';
```

You run the same `WHERE` as a `SELECT` first. You see on screen which
rows are about to change. If that is right, you turn the `SELECT` into
the `UPDATE`.

It takes two seconds and it prevents almost every mistake in this
section.

## Transactions: a change you can take back

There is also a real net. You can make a change **on trial** and decide
afterwards:

```sql
BEGIN TRANSACTION;

DELETE FROM shipments;

-- see what happened
SELECT COUNT(*) FROM shipments;

ROLLBACK;   -- changed my mind
-- COMMIT;  -- or: keep it
```

<figure class="fig">
  <div class="flow">
    <span class="node">BEGIN TRANSACTION</span>
    <span class="arrow">→</span>
    <span class="node">changes</span>
    <span class="arrow">→</span>
    <span class="node ok">COMMIT</span>
    <span class="arrow">/</span>
    <span class="node no">ROLLBACK</span>
  </div>
</figure>

Everything between `BEGIN TRANSACTION` and `COMMIT` is one package. None
of it is permanent until you say `COMMIT`; say `ROLLBACK` and all of it
is undone at once.

Odyssey's promise that "everything resets after each run" is exactly
this: your SQL runs inside a transaction and `ROLLBACK` is called at the
end.

**A transaction is not about a single command.** Its real power is tying
several changes together: if money leaves one account and enters another,
either both happen or neither does. That is what a transaction
guarantees.

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Add a row</span><span class="anat-body"><code>INSERT INTO t (columns) VALUES (...)</code> — write the column list</span></div>
    <div class="anat-row"><span class="anat-label">Change rows</span><span class="anat-body"><code>UPDATE t SET ... WHERE ...</code> — do not forget the <code>WHERE</code></span></div>
    <div class="anat-row"><span class="anat-label">Remove rows</span><span class="anat-body"><code>DELETE FROM t WHERE ...</code> — do not forget the <code>WHERE</code></span></div>
    <div class="anat-row"><span class="anat-label">Empty a table</span><span class="anat-body"><code>TRUNCATE TABLE t</code></span></div>
    <div class="anat-row"><span class="anat-label">Rehearse first</span><span class="anat-body">A <code>SELECT</code> with the same <code>WHERE</code></span></div>
    <div class="anat-row"><span class="anat-label">Make it reversible</span><span class="anat-body"><code>BEGIN TRANSACTION</code> ... <code>ROLLBACK</code></span></div>
  </div>
</figure>

In the next section you will build the tables themselves — and there you
will meet the constraints that stop bad data from getting in at all.
