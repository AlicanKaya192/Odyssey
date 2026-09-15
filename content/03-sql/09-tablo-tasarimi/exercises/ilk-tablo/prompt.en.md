Create a table called `warehouses`.

| Column | Type | Rule |
|---|---|---|
| `code` | `NVARCHAR(10)` | primary key |
| `city` | `NVARCHAR(30)` | cannot be empty |
| `capacity` | `INT` | cannot be empty |

Only create the table; do not add rows.

The check looks at the table's **structure**: the columns' names, types
and lengths, whether they may be empty, and which column is the primary
key. So choose the types exactly as written — `VARCHAR` and `NVARCHAR`
count as different.
