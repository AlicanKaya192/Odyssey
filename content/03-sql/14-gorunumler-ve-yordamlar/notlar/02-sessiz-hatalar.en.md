Most mistakes with views and procedures come with a message, and the
message says what to do. This note collects **the ones without a
message**: all were measured in this section, and in all of them the
query ran and the result was wrong or incomplete.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">A SELECT * view</span><span class="anat-body">A column added to the table does not show up in the view.</span></div>
    <div class="anat-row"><span class="anat-label">A vanishing row</span><span class="anat-body">A row changed through the view drops out of it.</span></div>
    <div class="anat-row"><span class="anat-label">An invisible insert</span><span class="anat-body">A row added through the view is in the table but not in the view.</span></div>
    <div class="anat-row"><span class="anat-label">A forgotten OUTPUT</span><span class="anat-body">The variable stays <code>NULL</code>.</span></div>
    <div class="anat-row"><span class="anat-label">A missing customer</span><span class="anat-body">The procedure returns an empty result.</span></div>
    <div class="anat-row"><span class="anat-label">A missing table</span><span class="anat-body">The procedure is created; the error comes only when it runs.</span></div>
  </div>
</figure>

## 1. A SELECT * view goes stale

After `CREATE VIEW dbo.v_suppliers AS SELECT * FROM suppliers`, a `phone`
column was added to the table. The table showed five columns, the view
four. After `sp_refreshview`, five.

**Fix:** name the columns in a view. If a new column is needed, change
the view on purpose (`CREATE OR ALTER VIEW`). If you want a tight bond,
`WITH SCHEMABINDING` — and then `*` cannot be written at all.

## 2. A row changed through a view disappears

Through `pending_orders`, 1004's status was set to `shipped`. No error;
the row was updated in the table and dropped out of the view.

## 3. A row added through a view does not show up

A row was added through the same view with `status = 'shipped'`. In the
table 1, in the view 0.

**Fix (2 and 3):** `WITH CHECK OPTION`. Both were refused with error
550; an insert with `'pending'` was accepted.

## 4. OUTPUT forgotten in the call

```sql
DECLARE @n INT;
EXEC dbo.customer_order_count 1, @n;      -- no OUTPUT
SELECT @n;                                -- NULL
```

The procedure ran and worked out the number, but did not write it into
`@n`. No error.

**Fix:** `OUTPUT` in two places: the definition and the call. Checking
the value once after the call (is it `NULL`?) shows this mistake right
away.

## 5. A missing record gives an empty result

`EXEC dbo.customer_orders @customer_id = 99` raised no error and came
back empty. A customer with no orders (6) gives the same empty result.
The caller cannot tell the two apart.

**Fix:** if the difference matters, let the procedure say so: a status
code with `RETURN 1` (measured: 1 for 99, 0 for 1) or an error with
`THROW`.

## 6. A procedure naming a missing table is created

`CREATE PROCEDURE dbo.p8 AS SELECT * FROM dbo.no_such_table` was created
without an error; at `EXEC`, `Invalid object name`. A missing **column**,
on the other hand, was caught at creation.

**Fix:** run a procedure once after creating it. Being created does not
mean being right.

## And one with a misleading message: GO

A `SELECT` written after `CREATE VIEW` without `GO` gave `Incorrect
syntax near the keyword 'SELECT'.` The message reads as if there were a
typo in the `SELECT`; the real reason is that `CREATE VIEW` is not in a
batch of its own. With `GO` in between it worked.

## The questions to ask

- **Is there a `*` in the view?** If so, its column list froze on the
  day it was created.
- **Is anyone writing through the view?** If so, `WITH CHECK OPTION`.
- **Is the procedure's output parameter marked `OUTPUT` in the call
  too?**
- **Are "not found" and "empty" different things?** If so, the procedure
  should say which.
