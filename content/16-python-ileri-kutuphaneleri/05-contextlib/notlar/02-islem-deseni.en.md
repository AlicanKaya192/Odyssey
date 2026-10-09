One of the most common places for a context manager is a **transaction**:
"either all the changes in the block are saved together, or none". Python's
`sqlite3` connection does this with `with`; but it has a trap.

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE t (x INTEGER)")
    with conn:
        conn.execute("INSERT INTO t VALUES (1)")
    try:
        with conn:
            conn.execute("INSERT INTO t VALUES (2)")
            raise ValueError("stop")
    except ValueError:
        pass
    print(conn.execute("SELECT x FROM t").fetchall())
try:
    conn.execute("SELECT 1")
except sqlite3.ProgrammingError as error:
    print("ProgrammingError:", error)
```

```text
[(1,)]
ProgrammingError: Cannot operate on a closed database.
```

- **`with conn:`** is a transaction block: if the block ends normally the
  changes are saved (`commit`), if an error occurs they are undone
  (`rollback`). The `2` in the second block was undone because of the error;
  only `1` is in the table.
- **The trap:** `with conn:` does **not close** the connection. To close it,
  use **`contextlib.closing`**: it turns any object with a `close()` method
  into a context manager and calls `close()` at the end of the block. When
  the outer block ended the connection was closed; the next query failed.

## Your own transaction pattern

The same idea applies to other resources: save if the block succeeds, undo
otherwise.

```python
from contextlib import contextmanager


@contextmanager
def transaction(data):
    snapshot = dict(data)
    try:
        yield data
    except Exception:
        data.clear()
        data.update(snapshot)
        raise
```

If an error occurs in the block, the dictionary goes back to its copy from
before the block; `raise` still passes the error outward (it does not
swallow it). The first exercise is the complete version of this.
