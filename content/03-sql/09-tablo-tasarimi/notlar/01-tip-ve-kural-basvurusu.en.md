One page to keep at hand while building tables. The error texts were
taken from the real server on this section's schema.

## The shape

```sql
CREATE TABLE table_name (
    column1 TYPE RULES,
    column2 TYPE RULES,
    CONSTRAINT rule_name RULE
);
```

Rules can go at the end of a column; a rule that concerns more than one
column (a composite key, a `CHECK` comparing two columns) goes at the end
of the table, on its own line.

## Types

| Need | Type | Note |
|---|---|---|
| Id, count | `INT` | |
| Money, measurements | `DECIMAL(10,2)` | Extra digits are **silently rounded** (`12.345` → `12.35`) |
| Text | `NVARCHAR(n)` | Text that is too long is refused, not cut |
| Date | `DATE` | Written as `'2026-09-15'` |

## Rules and their error texts

| Rule | Refuses when | Message |
|---|---|---|
| `NOT NULL` | No value is given | `Cannot insert the value NULL into column ...` |
| `PRIMARY KEY` | The same key a second time | `Violation of PRIMARY KEY constraint ...` |
| `UNIQUE` | The same value a second time | `Violation of UNIQUE KEY constraint ...` |
| `CHECK` | The condition is definitely false | `... conflicted with the CHECK constraint ...` |
| `REFERENCES` | The parent does not exist | `... conflicted with the FOREIGN KEY constraint ...` |
| `REFERENCES` | Deleting a parent that has children | `... conflicted with the REFERENCE constraint ...` |
| `IDENTITY` | Giving the number yourself | `Cannot insert explicit value for identity column ...` |

## Behaviour that surprises people

All measured:

- A column with `CHECK (price > 0)` that may be empty **accepts** `NULL`.
  If it must not be empty, add `NOT NULL` as well.
- A second `NULL` **cannot** go into a `UNIQUE` column (specific to SQL
  Server).
- `DEFAULT` only works when the column is not written at all; writing
  `NULL` explicitly leaves `NULL`.
- `IDENTITY` does **not reuse** a deleted number: 1, 3.

## Link options

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">REFERENCES t(id)</span><span class="anat-body">The default: a parent with children cannot be deleted.</span></div>
    <div class="anat-row"><span class="anat-label">ON DELETE CASCADE</span><span class="anat-body">When the parent is deleted, the children are deleted too.</span></div>
    <div class="anat-row"><span class="anat-label">A link that may be empty</span><span class="anat-body">A <code>NULL</code> value points at no parent and is accepted.</span></div>
  </div>
</figure>

## ALTER TABLE

```sql
ALTER TABLE t ADD col TYPE NULL;                     -- old rows get NULL
ALTER TABLE t ADD col TYPE NOT NULL DEFAULT value;   -- old rows get value
ALTER TABLE t DROP COLUMN col;
ALTER TABLE t ADD CONSTRAINT name CHECK (condition);
ALTER TABLE t ADD CONSTRAINT name FOREIGN KEY (col) REFERENCES p(id);
```

| Attempt | Result (measured) |
|---|---|
| A `NOT NULL` column on a table with data, no `DEFAULT` | refused |
| A `CHECK` the existing data breaks | refused |
| A foreign key while orphan rows exist | refused |
| Narrowing a column so far that data would be cut | refused |
| Using a new column in the same batch | `Invalid column name` — put `GO` in between |

## Inspecting a table

```sql
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'tasks'
ORDER BY ORDINAL_POSITION;
```

This shows a table's columns, their types and whether they may be empty.
`INFORMATION_SCHEMA.TABLE_CONSTRAINTS` lists its rules as well. That is
exactly how this section's exercises are checked.
