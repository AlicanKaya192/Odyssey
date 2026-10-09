# sqlite3

In the Python path's Database section you built a table with `sqlite3`,
inserted and queried data, and saw why the `?` placeholder matters and what
`commit` does. This section covers the advanced topics a real application's
database layer needs: reaching rows by name, bulk inserts, how SQL injection
really works, **transactions**, **indexes** and query plans, and storing
dates.

## Row and executemany

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute(
    "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
rows = [("pen", 1.5), ("ink", 0.5), ("book", 12.0)]
conn.executemany("INSERT INTO products (name, price) VALUES (?, ?)", rows)
for row in conn.execute("SELECT * FROM products WHERE price > ?", (1,)):
    print(row["id"], row["name"], row["price"], dict(row))
print(conn.execute("SELECT COUNT(*) FROM products").fetchone()[0])
```

```text
1 pen 1.5 {'id': 1, 'name': 'pen', 'price': 1.5}
3 book 12.0 {'id': 3, 'name': 'book', 'price': 12.0}
3
```

- **`":memory:"`** builds the database in memory instead of a file: for
  experiments and tests.
- **`conn.row_factory = sqlite3.Row`**: rows become `Row` objects reachable
  **by name** (`row["name"]`) instead of tuples; `dict(row)` turns one into a
  dictionary. The code does not break when the column order changes.
- **`executemany`** runs the same query for a list in one call; with
  thousands of rows it is much faster than `execute` in a loop.
- `INTEGER PRIMARY KEY` is an auto-incrementing id (1, 2, 3).

## Injection: why ? is written

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, admin INTEGER)")
conn.execute("INSERT INTO users VALUES ('ada', 1), ('alan', 0)")
name = "x' OR '1'='1"
unsafe = f"SELECT name FROM users WHERE name = '{name}'"
print(conn.execute(unsafe).fetchall())
print(conn.execute("SELECT name FROM users WHERE name = ?", (name,)).fetchall())
named = "SELECT name FROM users WHERE name = :n"
print(conn.execute(named, {"n": "ada"}).fetchall())
```

```text
[('ada',), ('alan',)]
[]
[('ada',)]
```

The user's `x' OR '1'='1`, glued into the query with an f-string, closed the
quote and **changed the meaning of the query**: the condition became true for
every row and all users came back. A value given with `?` goes only as
**data**; there is no such name, the result is empty. A named placeholder
(`:n` + a dictionary) is more readable in queries with many parameters. The
rule: **no value is ever formatted into SQL text.**

## A transaction: all together or nothing

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts "
             "(name TEXT PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
conn.executemany("INSERT INTO accounts VALUES (?, ?)", [("ada", 100), ("alan", 20)])
conn.commit()
ADD = "UPDATE accounts SET balance = balance + ? WHERE name = ?"
SUB = "UPDATE accounts SET balance = balance - ? WHERE name = ?"


def transfer(src, dst, amount):
    try:
        with conn:
            conn.execute(ADD, (amount, dst))
            conn.execute(SUB, (amount, src))
    except sqlite3.IntegrityError as error:
        print("IntegrityError:", error)


transfer("ada", "alan", 30)
transfer("alan", "ada", 500)
print(conn.execute("SELECT * FROM accounts ORDER BY name").fetchall())
```

```text
IntegrityError: CHECK constraint failed: balance >= 0
[('ada', 70), ('alan', 50)]
```

- A money transfer is two updates: add to one, subtract from the other. If
  the second fails, the first must be undone too; otherwise money appears
  from nowhere.
- A **`with conn:`** block is a **transaction**: `commit` with no error,
  `rollback` with one. In the second transfer 500 was added to `ada`, but
  subtracting from `alan` broke the `CHECK (balance >= 0)` rule; the
  transaction was undone and `ada` stayed at 70.
- Constraints like **`CHECK`** protect the data in the database itself:
  whatever code writes, a negative balance cannot be saved.

## Indexes and the query plan

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, user TEXT, kind TEXT)")
data = [(f"user{i % 5000}", "click" if i % 3 else "view") for i in range(200_000)]
conn.executemany("INSERT INTO events (user, kind) VALUES (?, ?)", data)
query = "SELECT COUNT(*) FROM events WHERE user = ?"
plan = conn.execute("EXPLAIN QUERY PLAN " + query, ("user42",)).fetchall()
print(plan[0][-1])
conn.execute("CREATE INDEX idx_events_user ON events (user)")
plan = conn.execute("EXPLAIN QUERY PLAN " + query, ("user42",)).fetchall()
print(plan[0][-1])
print(conn.execute(query, ("user42",)).fetchone()[0])
```

```text
SCAN events
SEARCH events USING COVERING INDEX idx_events_user (user=?)
40
```

- **`EXPLAIN QUERY PLAN`** says **how** the database will run the query.
  Without an index, `SCAN`: all 200,000 rows are looked at.
- **`CREATE INDEX`** builds a sorted lookup structure for the column; the
  plan became `SEARCH ... USING INDEX`: it goes straight to the relevant
  rows. Indexes go on columns you often filter (`WHERE`) and join on.
- The cost of an index: it must be updated on every insert and update, and
  it takes disk space. Not every column gets an index.

## Storing dates

```python
import sqlite3
from datetime import date

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (day TEXT, total REAL)")
conn.executemany("INSERT INTO orders VALUES (?, ?)",
                 [(date(2026, 3, d).isoformat(), d * 10.0) for d in (1, 2, 15)])
rows = conn.execute("SELECT day, total FROM orders WHERE day >= ? ORDER BY day",
                    ("2026-03-02",)).fetchall()
print(rows)
print([date.fromisoformat(day) for day, _ in rows][0].weekday())
monthly = "SELECT strftime('%m', day), SUM(total) FROM orders GROUP BY 1"
print(conn.execute(monthly).fetchall())
```

```text
[('2026-03-02', 20.0), ('2026-03-15', 150.0)]
0
[('03', 180.0)]
```

SQLite has no separate date type; a date is stored as **ISO text**
(`2026-03-02`). Because the ISO format sorted as text is in date order, `>=`
and `ORDER BY` work correctly. When reading, it is converted back with
`date.fromisoformat`; inside SQL, `strftime` pulls out the month or year.

## Common mistakes

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (x INTEGER)")
cur = conn.execute("INSERT INTO t VALUES (?)", (5,))
print(cur.rowcount, cur.lastrowid)
try:
    conn.execute("INSERT INTO t VALUES (?)", 5)
except sqlite3.ProgrammingError as error:
    print(type(error).__name__)
print(conn.execute("SELECT * FROM t WHERE x = ?", (5,)).fetchall())
```

```text
1 1
ProgrammingError
[(5,)]
```

- Parameters are given as a **sequence**: for a single value `(5,)` (a tuple
  with a comma) or `[5]`. A plain `5` raises `ProgrammingError`.
- `cursor.rowcount` is the number of affected rows, `lastrowid` the id of the
  inserted row: for "how many rows were updated" and "what is the new
  record's id".
- A forgotten `commit` and a connection never closed: `with conn:` for the
  transaction, `contextlib.closing` for closing (the contextlib section).

## Summary

- `row_factory = sqlite3.Row` for access by name; `executemany` for bulk
  inserts.
- Values always with `?` or `:name`; never with an f-string.
- `with conn:` is a transaction: `commit` on success, `rollback` on error;
  `CHECK`, `UNIQUE`, `NOT NULL` constraints.
- `EXPLAIN QUERY PLAN` + `CREATE INDEX`: `SEARCH` instead of `SCAN`.
- Dates as ISO text; `date.fromisoformat`, `strftime` in SQL.
