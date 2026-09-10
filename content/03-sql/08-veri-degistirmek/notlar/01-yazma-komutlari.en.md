A one-page summary of the three commands. The error texts were taken
from the real server on this section's schema.

## The forms

```sql
-- add
INSERT INTO table (col1, col2) VALUES (value1, value2);

-- many rows
INSERT INTO table (col1, col2) VALUES
    (a1, a2),
    (b1, b2);

-- from another query
INSERT INTO table (col1, col2)
SELECT x, y FROM other_table WHERE ...;

-- change
UPDATE table SET col = value WHERE condition;

-- remove
DELETE FROM table WHERE condition;

-- empty the table
TRUNCATE TABLE table;
```

## Which command for which question

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">A new row</span><span class="anat-body"><code>INSERT</code></span></div>
    <div class="anat-row"><span class="anat-label">An existing row</span><span class="anat-body"><code>UPDATE</code></span></div>
    <div class="anat-row"><span class="anat-label">Some rows should go</span><span class="anat-body"><code>DELETE</code> + <code>WHERE</code></span></div>
    <div class="anat-row"><span class="anat-label">All of them, keep the table</span><span class="anat-body"><code>TRUNCATE TABLE</code></span></div>
    <div class="anat-row"><span class="anat-label">The table should go too</span><span class="anat-body"><code>DROP TABLE</code></span></div>
  </div>
</figure>

## Error messages and what they mean

| Message | What happened |
|---|---|
| `Cannot insert the value NULL into column 'name' ... column does not allow nulls` | You gave no value for a `NOT NULL` column |
| `There are more columns in the INSERT statement than values specified` | The number of columns and values do not match |
| `Violation of PRIMARY KEY constraint ... The duplicate key value is (ACC)` | That key is already in the table |
| `Conversion failed when converting the varchar value 'abc' to data type int` | You wrote text where a number was expected |
| `Invalid object name 'x'` | The table name is wrong, or the table does not exist |

All of these are **good news**: the server kept bad data out. The
dangerous statements are the ones that raise no error.

## How many rows were affected

```sql
UPDATE products SET stock = stock + 1 WHERE category_code = 'ACC';
SELECT @@ROWCOUNT AS affected;   -- 6
```

`@@ROWCOUNT` holds the count of the **last** command, and every command
in between overwrites it. Measured: put a query returning one row
between the `UPDATE` and `SELECT @@ROWCOUNT` and the answer is **`1`**,
not `6` — it counts the query in between. That is why it is read
immediately after.

What the number tells you:

- **Higher than you expected** → the `WHERE` is catching too many rows.
- **Zero** → the `WHERE` caught nothing. Not an error, but probably not
  what you wanted either.
- **What you expected** → you are on the right track.

## Fuller forms of UPDATE and DELETE

When the condition looks at another table there are two ways:

```sql
-- with a subquery
DELETE FROM order_items
WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled');

-- with a join (specific to T-SQL)
DELETE oi FROM order_items oi
JOIN orders o ON o.id = oi.order_id
WHERE o.status = 'cancelled';
```

Both give the same result. The subquery form works on every database;
the `DELETE ... FROM ... JOIN` form is specific to T-SQL.

The same applies to `UPDATE`:

```sql
UPDATE p SET p.stock = 0
FROM products p
JOIN categories c ON c.code = p.category_code
WHERE c.name = 'Software';
```

Careful: the name you write after `UPDATE` has to be one that **appears**
in `FROM`. If you gave an alias you can write either the alias or the
table name, but a name that never appears in `FROM` is an error:
`Invalid object name 'p'` (measured).

## Transaction commands

```sql
BEGIN TRANSACTION;   -- start
COMMIT;              -- make it permanent
ROLLBACK;            -- undo all of it
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Inside a transaction</span><span class="anat-body">Only you see the changes. Somebody else's query still reads the old state.</span></div>
    <div class="anat-row"><span class="anat-label">After COMMIT</span><span class="anat-body">Everyone sees it. There is no way back.</span></div>
    <div class="anat-row"><span class="anat-label">After ROLLBACK</span><span class="anat-body">As though nothing happened.</span></div>
  </div>
</figure>

**Writing `COMMIT` in Odyssey has no effect.** The exercise already runs
inside a transaction, and the database is rebuilt from the seed either
way. On a real server `COMMIT` is the command with no way back.

## The three common mistakes

1. **Forgetting the `WHERE`.** For `UPDATE` and `DELETE` the form
   without one means "all of them", and the server does not question it.
2. **Leaving out the column list in an `INSERT`.** It works today and
   breaks silently the day a column is added to the table.
3. **Writing `DROP` where you meant `DELETE`.** `DELETE` removes rows,
   `DROP` removes the table.
