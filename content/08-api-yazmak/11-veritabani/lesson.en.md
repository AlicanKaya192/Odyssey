# A Database: SQLite

Until now the records lived in a dictionary. When the server stops, they're
all gone. A real API keeps its data in a **database**. In this section you
work with **SQLite**, which comes inside Python: no installation, no server,
the database is a single file (`library.db`).

In the SQL track you wrote `SELECT`, `INSERT`, `WHERE`; here you send the
same commands from Python with the `sqlite3` module.

## Creating the table

```python
import sqlite3

DB_PATH = "library.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        year INTEGER NOT NULL)""")
    conn.commit()
    conn.close()


init_db()
```

- `sqlite3.connect(DB_PATH)`: opens the file, creating it if missing.
- `IF NOT EXISTS`: this runs every time the program starts; if the table
  exists, it's left alone.
- `id INTEGER PRIMARY KEY AUTOINCREMENT`: the database gives the number. The
  `next_id` counter from the CRUD section isn't needed any more.
- `UNIQUE`: the same title can't be entered twice.

## A connection per request: a `yield` dependency

In the Dependencies section you saw the "open and close" pattern. Here is
its real use:

```python
from typing import Annotated
from fastapi import Depends


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


DB = Annotated[sqlite3.Connection, Depends(get_db)]
```

- Every request gets its own connection; it's closed after the answer.
- `row_factory = sqlite3.Row`: rows can be read by column name
  (`row["title"]`) and turned into a dictionary with `dict(row)`.
- `check_same_thread=False`: FastAPI may run the dependency and the endpoint
  in different threads; by default `sqlite3` refuses to use a connection in
  another thread. We saw no error in our measurement, but since the
  connection is opened per request, this setting is the safe and common
  way.

## Adding: `INSERT` + `commit`

```python
@app.post("/books", status_code=201)
def create_book(book: BookIn, db: DB):
    try:
        cur = db.execute("INSERT INTO books (title, year) VALUES (?, ?)",
                         (book.title, book.year))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Title already exists")
    return {"id": cur.lastrowid, **book.model_dump()}
```

- `?` placeholders with the values given separately: a **parameterised
  query**. You'll see below why it matters.
- `cur.lastrowid`: the number the database gave the new row.
- `db.commit()`: makes the change permanent. If you **forget** it, the
  answer still says `201` but the data isn't saved. We measured: after adding
  a book without `commit`, `GET /books` → `[]`.
- When `UNIQUE` is broken, `sqlite3.IntegrityError`; we turn it into `409`.

## Reading

```python
@app.get("/books/{book_id}")
def read_book(book_id: int, db: DB):
    row = db.execute("SELECT id, title, year FROM books WHERE id = ?",
                     (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)
```

- `fetchone()`: one row or `None`. `fetchall()`: a list of rows.
- `(book_id,)`: even a single value is given as a **tuple**; don't forget the
  comma.

## Deleting: how many rows changed?

```python
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: DB):
    cur = db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
```

`cur.rowcount` is the number of affected rows. No need to `SELECT` first and
delete afterwards: if no row was deleted, the record didn't exist.

<figure class="fig">
  <div class="flow">
    <span class="node">Request</span><span class="arrow">→</span>
    <span class="node acc">get_db()<br><small>connect</small></span><span class="arrow">→</span>
    <span class="node">Endpoint<br><small>execute + commit</small></span><span class="arrow">→</span>
    <span class="node ok">Answer</span><span class="arrow">→</span>
    <span class="node acc">finally<br><small>close</small></span>
  </div>
  <figcaption>Each request opens its own connection, does its work, and the connection is closed after the answer goes out. The data stays in the <code>library.db</code> file.</figcaption>
</figure>

## The flow we measured

```text
POST /books  Dune 1965        201 {"id": 1, "title": "Dune", "year": 1965}
POST /books  Emma 1815        201 {"id": 2, ...}
POST /books  Dune 1965        409 {"detail": "Title already exists"}
GET /books?year=1815          200 [{"id": 2, "title": "Emma", "year": 1815}]
GET /books/9                  404
DELETE /books/1               204
DELETE /books/1               404
POST /books  Ubik 1969        201 {"id": 3, ...}
```

The deleted number `1` wasn't given again: `AUTOINCREMENT` doesn't reuse
numbers. Since the data is in a file, the books are still there even if the
server restarts.

## SQL injection: why `?`

Building the query by joining text looks tempting:

```python
db.execute(f"SELECT id, title FROM books WHERE title = '{title}'")
```

It works for `title=Dune`. But if someone sends this:

```text
GET /unsafe?title=x' OR '1'='1
200 [{"id": 1, "title": "Dune"}, {"id": 2, "title": "Emma"}]
```

The incoming text became **part** of the query:
`WHERE title = 'x' OR '1'='1'` selected every row (we measured). A table
could be dropped the same way. This is called **SQL injection**.

A value given with `?` always stays a **value**, never a command. The rule is
absolute: **never join anything that came from the user into the query
text.** Even in a `LIKE` search:

```python
db.execute("SELECT title FROM books WHERE title LIKE ?", (f"%{q}%",))
```

The `%` signs are inside the value, not the query.

## Summary

- `sqlite3` comes with Python; the database is one file.
- The table is created at startup with `CREATE TABLE IF NOT EXISTS`.
- A connection per request: a `yield` `get_db` + `row_factory = sqlite3.Row`.
- `commit()` after a change; otherwise the data is lost.
- `lastrowid` is the new number, `rowcount` the affected rows;
  `IntegrityError` → `409`.
- Values always with `?`: don't open the door to SQL injection.
