## Connection

| Code | What it does |
|---|---|
| `sqlite3.connect("app.db")` / `(":memory:")` | a file / memory |
| `conn.row_factory = sqlite3.Row` | access rows by name |
| `with conn:` | a transaction: commit on success, rollback on error |
| `contextlib.closing(conn)` | close at the end of the block |

## Queries

| Code | What it gives |
|---|---|
| `conn.execute(sql, (a, b))` | a cursor |
| `conn.execute(sql, {"name": a})` | with a named placeholder (`:name`) |
| `conn.executemany(sql, rows)` | bulk insert |
| `cur.fetchone()` / `fetchall()` | one row / all |
| `for row in conn.execute(...)` | row by row |
| `cur.rowcount`, `cur.lastrowid` | affected rows, the new id |

## Table

```sql
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total REAL CHECK (total >= 0),
    day TEXT
);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders (customer);
```

## Types

| Python | SQLite |
|---|---|
| `int`, `bool` | `INTEGER` (`bool` as 0/1) |
| `float` | `REAL` |
| `str` | `TEXT` |
| `date`, `datetime` | `TEXT` (ISO) |
| `None` | `NULL` |

## Rules

- Values with `?` or `:name`; no formatting into SQL text.
- Writes that belong together in one `with conn:` block.
- An index on a frequently filtered column; check with `EXPLAIN QUERY PLAN`.
- A single parameter is `(x,)`.
