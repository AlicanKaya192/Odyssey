The syntax is easy; the hard part is building a table that will hold up
for years. This note collects those decisions. The numbers and error
texts were measured on the real server.

## Each fact in one place

In the sixth section the supplier's name lived in its own table rather
than the product table. The reason still holds: when the same fact is
written in two places, one day one of them is forgotten in an update and
the data contradicts itself.

The question to ask: **"Does this column describe the row itself, or
something else?"** A product's price describes the product; a supplier's
city describes the supplier. A column describing something else goes to
its own table, leaving behind only a key that points at it.

## Choosing the key

<figure class="fig">
  <div class="versus">
    <div>
      <h4>A natural key</h4>
      From the data itself: a product code, a supplier code. Readable; but it can change in the real world, and when it does, every row pointing at it has to change too.
    </div>
    <div>
      <h4>A surrogate key</h4>
      A number handed out by the server with <code>IDENTITY</code>. It means nothing, so it never needs to change.
    </div>
  </div>
</figure>

A common choice is both: the surrogate key becomes the primary key and
the natural code sits beside it as `UNIQUE`.

```sql
CREATE TABLE parts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sku NVARCHAR(20) NOT NULL UNIQUE,
    ...
);
```

**Watch the letter case.** On this server key comparison does not tell
capitals from small letters: `w1` and `W1` counted as the same key and
the second was refused (measured). Writing codes in one form avoids the
surprise.

## DECIMAL for money, not FLOAT

`FLOAT` holds a number **approximately**, in binary. Measured:

| Calculation | Result | `= 0.3`? |
|---|---|---|
| `FLOAT`: `0.1 + 0.2` | `0.30000000000000004` | **no** |
| `DECIMAL(10,2)`: `0.1 + 0.2` | `0.3` | yes |

One tiny difference looks harmless, but summed over thousands of rows it
grows, and equality comparisons go quietly wrong. `FLOAT` where an
approximate value is enough, like scientific measurements; `DECIMAL` for
money, quantities and anything that has to be exact.

## Store dates as dates

Keeping a date in a text column looks harmless at first. Measured —
sorted as text:

```
2026-10-01
2026-9-15
2026-9-2
```

October came before September: text is compared character by character
and the character `1` is smaller than `9`. The same values went into the
right order in a `DATE` column. On top of that `DATE` **refused** a day
that does not exist (`2026-02-30`); a text column would have taken it.

## What should happen on delete

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Valuable on its own</span><span class="anat-body">Customer → orders. <b>The default (refuse).</b> If someone tries to delete the customer by mistake, the server stops them.</span></div>
    <div class="anat-row"><span class="anat-label">Meaningless without its parent</span><span class="anat-body">Order → notes, team → memberships. <code>ON DELETE CASCADE</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Instead of deleting</span><span class="anat-body">A status column (<code>status = 'cancelled'</code>). The history is kept.</span></div>
  </div>
</figure>

If in doubt, keep the default. Adding `CASCADE` later is easy; getting
back what a wrong `CASCADE` took is not.

## Rules across several columns

Some rules do not fit in a single column; they are written separately at
the end of the table.

```sql
-- composite key: the same order + the same product once
PRIMARY KEY (order_id, product_id)

-- a rule comparing two columns
CONSTRAINT ck_trip_dates CHECK (ends >= starts)
```

Adding the same (order, product) pair a second time to the order items
raised `... The duplicate key value is (1001, 1).`; a trip ending before
it starts was stopped by the `ck_trip_dates` rule (measured).

## Name your rules

The error for an unnamed rule says something like
`CK__items__price__6B24EA82`. Naming it with a short prefix makes the
error readable:

| Prefix | Rule |
|---|---|
| `pk_` | primary key |
| `fk_` | foreign key |
| `uq_` | `UNIQUE` |
| `ck_` | `CHECK` |

## Getting the new row's number

With `IDENTITY` the server hands out the number; so what number did the
row you added get?

```sql
INSERT INTO tickets (title)
OUTPUT inserted.id, inserted.title
VALUES ('a'), ('b');
```

`OUTPUT` returned the added rows with their numbers: `1 a`, `2 b`
(measured). It gives the number of every row when several are added at
once, which makes it handier than the ways that return a single value.

## A checklist before you build

<figure class="fig">
  <div class="flow">
    <span class="node">Does each column describe the row?</span>
    <span class="arrow">→</span>
    <span class="node">What is the key?</span>
    <span class="arrow">→</span>
    <span class="node">Which may not be empty?</span>
    <span class="arrow">→</span>
    <span class="node">Which values are invalid?</span>
    <span class="arrow">→</span>
    <span class="node">What happens on delete?</span>
  </div>
</figure>
