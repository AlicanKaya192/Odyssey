# Table Design

For eight sections you have worked with tables that were already there.
In this section you **build them yourself**.

A table is not only where data sits; it is also where the **rules** the
data has to follow are written down. Once a rule is in the table, every
`INSERT` and every `UPDATE` has to obey it — nobody can forget it, nobody
can skip it.

## CREATE TABLE

```sql
CREATE TABLE warehouses (
    code NVARCHAR(10) PRIMARY KEY,
    city NVARCHAR(30) NOT NULL,
    capacity INT NOT NULL
);
```

Each column says three things: its **name**, its **type** and its
**rules**. Columns are separated by commas.

If a table with the same name already exists the server stops you:
`There is already an object named 'products' in the database.`

## Data types

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">INT</span><span class="anat-body">A whole number: an id, a count, a stock level.</span></div>
    <div class="anat-row"><span class="anat-label">DECIMAL(10,2)</span><span class="anat-body">An <b>exact</b> decimal: 10 digits in total, 2 after the point. This is the one for money.</span></div>
    <div class="anat-row"><span class="anat-label">NVARCHAR(n)</span><span class="anat-body">Text of at most <code>n</code> characters, in any language.</span></div>
    <div class="anat-row"><span class="anat-label">DATE</span><span class="anat-body">A date without a time: <code>'2026-09-15'</code>.</span></div>
  </div>
</figure>

A type behaves like a rule; a value that does not fit is either adjusted
or refused. All three were measured:

| Value | Column | Result |
|---|---|---|
| `12.345` | `DECIMAL(10,2)` | stored as `12.35` — **rounded** |
| `1234.5` | `DECIMAL(5,2)` | error: `Arithmetic overflow error` |
| `'ABCDEFG'` | `NVARCHAR(5)` | error: `String or binary data would be truncated ... Truncated value: 'ABCDE'` |

The first one is the one to watch: the rounding is **silent**. Where every
cent matters, choose the number of digits after the point correctly from
the start.

### NVARCHAR or VARCHAR

Both hold text. The difference: `VARCHAR` stores characters according to
the server's **language setting**, `NVARCHAR` stores every letter of every
language.

Measured — writing `Şişli ğ ı` into a `VARCHAR` column with a Latin
language setting put **`Sisli g i`** into the table. No error, no warning;
the letters changed silently. The same value stayed as it was in an
`NVARCHAR` column.

The server on this machine is set to Turkish, so there `VARCHAR` keeps
Turkish letters too. But the day your table moves to another server, it
breaks. **Choose `NVARCHAR` for text.**

Putting `N` in front of the text you write is for the same reason:

```sql
INSERT INTO t (name) VALUES (N'Şişli');   -- safe
INSERT INTO t (name) VALUES ('Şişli');    -- depends on the server's language
```

Written without the `N`, `'日本'` went into an `NVARCHAR` column as `??`
(measured): the text is converted to the server's language before it
reaches the column.

## Rules

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NOT NULL</span><span class="anat-body">Cannot be empty.</span></div>
    <div class="anat-row"><span class="anat-label">PRIMARY KEY</span><span class="anat-body">Identifies each row on its own: never empty, never repeated. One per table.</span></div>
    <div class="anat-row"><span class="anat-label">UNIQUE</span><span class="anat-body">Cannot repeat — an email address, a product code.</span></div>
    <div class="anat-row"><span class="anat-label">CHECK (...)</span><span class="anat-body">A value that fails the condition does not get in: <code>CHECK (price &gt; 0)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">DEFAULT ...</span><span class="anat-body">Written when no value is given.</span></div>
    <div class="anat-row"><span class="anat-label">REFERENCES</span><span class="anat-body">Must point at a row in another table (a foreign key).</span></div>
  </div>
</figure>

```sql
CREATE TABLE parts (
    id INT PRIMARY KEY,
    sku NVARCHAR(20) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    status NVARCHAR(20) NOT NULL DEFAULT 'active'
);
```

Every write that breaks a rule is refused. The error texts were measured:

| Rule | Message |
|---|---|
| `NOT NULL` | `Cannot insert the value NULL into column 'city' ...` |
| `UNIQUE` | `Violation of UNIQUE KEY constraint ... The duplicate key value is (a@x.com).` |
| `CHECK` | `The INSERT statement conflicted with the CHECK constraint ... column 'price'.` |

### Three subtle points

All three were measured and all three surprise people:

- **`CHECK` lets an empty value through.** A column with `CHECK (price >
  0)` that is allowed to be empty accepted `NULL`: `NULL > 0` is
  "unknown", and `CHECK` only refuses a definite "false". If it must not
  be empty, add `NOT NULL` as well.
- **In SQL Server a `UNIQUE` column takes only one `NULL`.** A second
  empty phone number raised `Violation of UNIQUE KEY constraint ...
  (<NULL>)`. Other databases allow it; this is SQL Server's own behaviour.
- **`DEFAULT` only applies when the column is not written at all.** Writing
  `NULL` explicitly (on a column that may be empty) put `NULL` in the
  table, not the default.

### Naming your rules

If you do not name a rule the server makes a name up, and that is what
the error shows: `CK__items__price__6B24EA82`. If you name it, the error
says what it is:

```sql
price DECIMAL(10,2) NOT NULL
    CONSTRAINT ck_items_price CHECK (price > 0)
```

The error now says `... the CHECK constraint "ck_items_price"` (measured).

## IDENTITY: a number that counts up by itself

```sql
CREATE TABLE tickets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(60) NOT NULL
);

INSERT INTO tickets (title) VALUES ('a'), ('b'), ('c');
```

`IDENTITY(1,1)`: start at 1, go up by one. The server hands out the
numbers: 1, 2, 3 (measured). You do not write `id` in the `INSERT` — if you
do, the error is `Cannot insert explicit value for identity column ...
when IDENTITY_INSERT is set to OFF.`

**A deleted number does not come back.** Delete 2, add a new row, and the
new row is 3; 1 and 3 are left in the table (measured). That is not a
bug: the number's only job is to identify the row, not to count.

## FOREIGN KEY: declaring the link

In the previous section, deleting an order and leaving its items created
**orphan rows** and the server said nothing — because the link was not
declared. Once you declare it, the server starts protecting it:

```sql
CREATE TABLE teams (
    id INT PRIMARY KEY,
    name NVARCHAR(30) NOT NULL
);

CREATE TABLE members (
    id INT PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id)
);
```

Measured:

| Attempt | Result |
|---|---|
| Adding a member to a team that does not exist | `The INSERT statement conflicted with the FOREIGN KEY constraint ...` |
| Deleting a team that has members | `The DELETE statement conflicted with the REFERENCE constraint ...` |
| A member with an empty `team_id` (where the column may be empty) | accepted |

### What happens to the children when the parent goes

<figure class="fig">
  <div class="versus">
    <div>
      <h4>The default: refuse</h4>
      A parent with children cannot be deleted. You delete the children first, then the parent. Losing data by accident is impossible.
    </div>
    <div>
      <h4>ON DELETE CASCADE</h4>
      When the parent is deleted, its children go with it. Convenient, but a single <code>DELETE</code> can take more rows than you expect.
    </div>
  </div>
</figure>

```sql
team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE
```

In a table of three members, deleting team 1 removed both of its members
and left the other team's member (measured).

`CASCADE` is right for rows that **mean nothing without their parent**,
like a membership or an order's notes. For records that are valuable on
their own, like a customer's orders, the default "refuse" is safer.

### The previous section's promise

The links in the order database were not declared. Declaring one:

```sql
ALTER TABLE order_items
ADD CONSTRAINT fk_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id);

DELETE FROM orders WHERE id = 1006;
```

`The DELETE statement conflicted with the REFERENCE constraint
"fk_items_order"` — the server **refused** to delete the order (measured).
Delete the items first, then the order, and the job is done: nine orders
remain.

One warning: if the table **already** has orphan rows, the link cannot be
added. Deleting the order first and then trying to add the link raised
`The ALTER TABLE statement conflicted with the FOREIGN KEY constraint`.
The orphans have to be cleaned up first.

## ALTER TABLE: changing an existing table

```sql
-- add a column
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;

-- remove a column
ALTER TABLE customers DROP COLUMN phone;

-- add a rule
ALTER TABLE products ADD CONSTRAINT ck_price CHECK (price > 0);
```

Three cases were measured on a table that already holds data:

- A column **that may be empty** is added with `NULL` in the old rows.
- A **`NOT NULL`** column cannot be added without a default: it is not
  clear what to write into the old rows. Added with `DEFAULT 'standard'`,
  all six existing customers got `standard`.
- A **rule the existing data breaks** cannot be added. `CHECK (stock > 0)`
  was refused, because two products have zero stock.

So the server wants the rule you add to hold for **today's data** too.

### A new column and GO

```sql
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;
UPDATE customers SET phone = '555' WHERE id = 1;
```

This raises `Invalid column name 'phone'` (measured). The server reads all
the commands together before running any of them, and at that moment
there is no column called `phone`.

The fix is to put `GO` in between: it splits the commands into two
separate pieces.

```sql
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;
GO
UPDATE customers SET phone = '555' WHERE id = 1;
```

That works. Odyssey recognises `GO` just like SSMS does.

## DROP TABLE

```sql
DROP TABLE warehouses;
```

The table and everything in it goes. A table that another table's link
points at cannot be dropped: `Could not drop object 'orders' because it
is referenced by a FOREIGN KEY constraint.` (measured). Links protect you
here too.

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Text</span><span class="anat-body"><code>NVARCHAR(n)</code> and <code>N'...'</code></span></div>
    <div class="anat-row"><span class="anat-label">Money</span><span class="anat-body"><code>DECIMAL(10,2)</code> — rounding is silent</span></div>
    <div class="anat-row"><span class="anat-label">Identity</span><span class="anat-body"><code>INT IDENTITY(1,1) PRIMARY KEY</code></span></div>
    <div class="anat-row"><span class="anat-label">Rules</span><span class="anat-body"><code>NOT NULL</code>, <code>UNIQUE</code>, <code>CHECK</code>, <code>DEFAULT</code></span></div>
    <div class="anat-row"><span class="anat-label">Links</span><span class="anat-body"><code>REFERENCES</code> — with <code>ON DELETE CASCADE</code> where it fits</span></div>
    <div class="anat-row"><span class="anat-label">Changing</span><span class="anat-body"><code>ALTER TABLE</code>; <code>GO</code> before using a new column</span></div>
  </div>
</figure>

In the next section you will work with dates and text: the gap between
two days, the start of a month, splitting text and putting it together.
