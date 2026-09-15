# Views and Stored Procedures

Every query you have written so far lived in your editor: you ran it,
saw the result, and the query stayed there. If someone else — or an
application — needed the same calculation, you would have to hand them
the query itself.

This section puts the query **inside the database**. A **view** gives a
query a lasting name; it is queried like a table. A **stored
procedure** is a piece of code that takes parameters, can contain more
than one step, and is called by name. Everything below was measured on
the eight-table schema of the Intermediate level.

## A view: a query with a name

```sql
CREATE VIEW dbo.customer_revenue AS
SELECT c.id, c.name,
       SUM(i.quantity * i.unit_price) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY c.id, c.name;
```

Now it works like a table:

```sql
SELECT name FROM dbo.customer_revenue WHERE revenue > 10000 ORDER BY name;
```

Result: Bright Office, Helix Studio. Whoever uses the view does not need
to know about the three tables, the joins or the cancelled rule.

<figure class="fig">
  <div class="versus">
    <div>
      <h4>WITH</h4>
      <p>Gives a query a name, but the name lives <strong>only for that statement</strong>.</p>
      <p>It stays in your editor.</p>
    </div>
    <div>
      <h4>VIEW</h4>
      <p>The name is <strong>lasting in the database</strong>: anyone can use it until it is dropped.</p>
      <p>Other queries, other people, applications.</p>
    </div>
  </div>
</figure>

**A view holds no data.** Only its definition is stored; every time it is
used, the query runs again against the tables. Measured: when the
quantity of a line in order 1007 was lowered from 4 to 3, the view
immediately showed `3620.00` for Orion Labs instead of `4510.00`.

## The rules

Measured:

| Written as | Result |
|---|---|
| another statement before `CREATE VIEW` in the same batch | `'CREATE VIEW' must be the first statement in a query batch.` |
| `CREATE VIEW` followed by a `SELECT` without `GO` | `Incorrect syntax near the keyword 'SELECT'.` |
| `GO` in between | works |
| `SELECT customer_id, COUNT(*)` (an unnamed column) | `Create View or Function failed because no column name was specified for column 2.` |
| `ORDER BY` in a view | `The ORDER BY clause is invalid in views ... unless TOP, OFFSET or FOR XML is also specified.` |
| a second `CREATE VIEW` with the same name | `There is already an object named 'customer_revenue' in the database.` |
| `CREATE OR ALTER VIEW` | changes the existing one |

`CREATE VIEW` has to be in a batch of its own. In this application
batches are separated by a `GO` line: if you want to create the view and
try it underneath, put `GO` in between. Comment lines at the top are no
problem (measured).

## The SELECT * trap

```sql
CREATE VIEW dbo.v_suppliers AS SELECT * FROM suppliers;
ALTER TABLE suppliers ADD phone NVARCHAR(20) NULL;
```

After the column was added, the table showed five columns and the view
**still four** (measured). `*` is turned into a column list when the view
is created and stored that way. After `EXEC sp_refreshview
'dbo.v_suppliers'` the fifth column appeared.

The rule: name the columns in a view. Which columns it gives is a
decision; `*` quietly leaves that decision to the table as it was at that
moment.

## Changing data through a view

An `UPDATE` can be written through a single-table view, and the change
goes to the table:

```sql
CREATE VIEW dbo.pending_orders AS
SELECT id, customer_id, order_date, status
FROM orders WHERE status = 'pending';

UPDATE dbo.pending_orders SET status = 'shipped' WHERE id = 1004;
```

In `orders`, 1004 became `shipped` and **disappeared from the view**: it
no longer meets the view's `WHERE`. Adding a row through the same view
with `status = 'shipped'` was possible too — the row went into the
table and was not in the view (measured). Writing through a view
something the view does not show is confusing.

Two limits (measured):

| Written as | Result |
|---|---|
| an `UPDATE` through an aggregating view (`customer_revenue`) | `Update or insert of view or function 'dbo.customer_revenue' failed because it contains a derived or constant field.` |
| an `INSERT` through a view into a table with a `NOT NULL` column the view lacks | `Cannot insert the value NULL into column 'order_date' ...` |

## WITH CHECK OPTION

Added at the end of a view, it makes the server refuse any change that
would not meet the view's `WHERE`:

```sql
CREATE VIEW dbo.pending_checked AS
SELECT id, customer_id, order_date, status
FROM orders WHERE status = 'pending'
WITH CHECK OPTION;
```

`UPDATE ... SET status = 'shipped'` and an `INSERT` with `status =
'shipped'` were both refused: `The attempted insert or update failed
because the target view either specifies WITH CHECK OPTION ...` (error
550). A row added with `'pending'` was accepted.

## Dependencies: when a table changes

A view is bound to its tables only by name. Measured:

| Situation | Result |
|---|---|
| the view's table was dropped, then the view was used | `Invalid object name 'dbo.t_tmp'.` and `Could not use view or function 'dbo.v_tmp' because of binding errors.` |

`WITH SCHEMABINDING` binds a view tightly to its table:

| With `WITH SCHEMABINDING` | Result |
|---|---|
| `SELECT *` | `Syntax '*' is not allowed in schema-bound objects.` |
| a one-part name (`FROM t_sb`) | `... Names must be in two-part format ...` — `dbo.t_sb` is needed |
| dropping the bound table | `Cannot DROP TABLE 'dbo.t_sb' because it is being referenced by object 'v_sb'.` |
| changing the type of a column the view uses | `The object 'v_sb' is dependent on column 'a'.` |
| adding a new column to the table | allowed |

## A stored procedure

```sql
CREATE PROCEDURE dbo.customer_orders
    @customer_id INT
AS
SELECT id, order_date, status
FROM orders
WHERE customer_id = @customer_id
ORDER BY order_date;
```

Calling it:

```sql
EXEC dbo.customer_orders @customer_id = 1;   -- by name
EXEC dbo.customer_orders 4;                  -- by position
```

Three rows for customer 1 (1001, 1003, 1006), two for customer 4 (1005,
1009). How it differs from a view: it takes parameters, and it can
contain an `ORDER BY`.

Measured:

| Call | Result |
|---|---|
| `EXEC dbo.customer_orders` (no parameter) | `Procedure or function 'customer_orders' expects parameter '@customer_id', which was not supplied.` |
| `@customer_id = 'abc'` | `Error converting data type varchar to int.` |
| `@customer_id = '4'` | worked — the text was converted to a number |
| `@customer_id = 99` (a customer that does not exist) | an empty result, no error |
| an extra parameter | `Procedure or function customer_orders has too many arguments specified.` |
| `SELECT * FROM dbo.customer_orders` | `Invalid object name 'dbo.customer_orders'.` — a procedure cannot go in `FROM` |

## A default value

```sql
CREATE PROCEDURE dbo.orders_by_status
    @status NVARCHAR(20) = N'pending'
AS
SELECT id, customer_id, status FROM orders
WHERE status = @status ORDER BY id;
```

`EXEC dbo.orders_by_status` ran without a parameter and brought back the
three pending orders; `@status = N'shipped'` six rows. `EXEC
dbo.orders_by_status DEFAULT` used the default as well.

## An output parameter: OUTPUT

A procedure can return a value instead of (or alongside) a result table:

```sql
CREATE PROCEDURE dbo.customer_order_count
    @customer_id INT,
    @order_count INT OUTPUT
AS
SELECT @order_count = COUNT(*) FROM orders WHERE customer_id = @customer_id;
```

```sql
DECLARE @n INT;
EXEC dbo.customer_order_count 1, @n OUTPUT;
SELECT @n;   -- 3
```

Measured: customer 1 **3**, customer 6, who has no orders, **0**.

`OUTPUT` is written in two places: in the definition **and** in the
call. Forgotten in the call, `@n` **stayed `NULL` with no error**
(measured). The other way round, calling a parameter with `OUTPUT` when
the definition does not declare it is an error: `The formal parameter
"@x" was not declared as an OUTPUT parameter ...`.

`RETURN`, by contrast, only returns a whole number, usually as a status
code (`RETURN 0` success, `RETURN 1` "no such customer"; picked up with
`EXEC @r = dbo.p6 1`). A procedure written with `RETURN 'abc'` was
created, but when run it gave `Conversion failed when converting the
varchar value 'abc' to data type int.`

## Raising an error: THROW

The real strength of a procedure is putting the rule next to the table:

```sql
CREATE PROCEDURE dbo.ship_order
    @order_id INT
AS
BEGIN
    SET NOCOUNT ON;
    IF NOT EXISTS (SELECT 1 FROM orders
                   WHERE id = @order_id AND status = 'pending')
        THROW 50001, N'Order is not pending.', 1;
    UPDATE orders SET status = 'shipped' WHERE id = @order_id;
END;
```

Measured: `EXEC dbo.ship_order 1004` set the order to `shipped`; `EXEC
dbo.ship_order 1001` (already shipped) stopped with the error `Order is
not pending.` and never reached the `UPDATE`. Called inside `TRY ...
CATCH`, `ERROR_NUMBER()` gave 50001, `ERROR_MESSAGE()` `Order is not
pending.`, and `ERROR_PROCEDURE()` `dbo.ship_order`.

If the statement before `THROW` does not end with a semicolon, the
procedure is not created: `Incorrect syntax near 'THROW'.`

## What is not checked at creation

| Inside the procedure | Result |
|---|---|
| a table that does not exist | the procedure **was created**; at `EXEC`, `Invalid object name 'dbo.no_such_table'.` |
| a column that does not exist in an existing table | an error at creation: `Invalid column name 'no_such_column'.` |

A procedure naming a table that does not exist is accepted, on the
grounds that the table might be created later. If a typo is in a table
name, you only find out when you run it.

## What is in the database

```sql
SELECT name, type_desc FROM sys.objects WHERE type IN ('V', 'P');
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.pending_orders'));
```

The first listed the views (`VIEW`) and procedures
(`SQL_STORED_PROCEDURE`), the second gave the view's definition as it
was written. `sys.parameters` showed a procedure's parameters, their
types and which one is `OUTPUT`.

Because every run is rolled back at the end in this application, a view
or procedure you create is not there on the next run (measured: after
the rollback `OBJECT_ID` was `NULL`).

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">CREATE VIEW</span><span class="anat-body">A lasting name for a query; it holds no data. Name the columns; no <code>ORDER BY</code>.</span></div>
    <div class="anat-row"><span class="anat-label">WITH CHECK OPTION</span><span class="anat-body">Whatever is written through the view has to meet its <code>WHERE</code>.</span></div>
    <div class="anat-row"><span class="anat-label">SCHEMABINDING</span><span class="anat-body">While the view exists, its table cannot be dropped or changed.</span></div>
    <div class="anat-row"><span class="anat-label">CREATE PROCEDURE</span><span class="anat-body">Code that takes parameters and is called by name; with <code>EXEC</code>.</span></div>
    <div class="anat-row"><span class="anat-label">OUTPUT</span><span class="anat-body">In the definition and in the call; forgotten in the call, a silent <code>NULL</code>.</span></div>
    <div class="anat-row"><span class="anat-label">THROW</span><span class="anat-body">Puts the rule next to the table; the statement before it ends with <code>;</code>.</span></div>
    <div class="anat-row"><span class="anat-label">GO</span><span class="anat-body"><code>CREATE VIEW</code> / <code>PROCEDURE</code> in a batch of its own.</span></div>
  </div>
</figure>

The next section is the last one of the SQL path: a general review.
