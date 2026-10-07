The parts of the `sqlite3` module you use while writing an API; all measured.

| Code | What it does |
|---|---|
| `conn = sqlite3.connect("library.db")` | Opens the file (creating it if missing) |
| `conn.row_factory = sqlite3.Row` | Rows become `row["title"]` and `dict(row)` |
| `cur = conn.execute(sql, (a, b))` | One command, values with `?` |
| `conn.executemany(sql, [(a, b), ...])` | The same command for many rows |
| `cur.fetchone()` | One row or `None` |
| `cur.fetchall()` | A list of rows (`[]` if empty) |
| `conn.commit()` | Makes the changes permanent |
| `cur.lastrowid` | The new row's number after `INSERT` |
| `cur.rowcount` | The affected rows after `UPDATE` / `DELETE` |
| `conn.close()` | Closes the connection |

## `sqlite3.Row`

```python
row = conn.execute("SELECT * FROM books WHERE id = 1").fetchone()
row["title"]      # 'Dune'
row[1]            # 'Dune' (by position works too)
row.keys()        # ['id', 'title', 'year']
dict(row)         # {'id': 1, 'title': 'Dune', 'year': 1966}
```

FastAPI can't turn a `Row` object into JSON directly; return `dict(row)`.

## Even one value is a tuple

```python
conn.execute("SELECT * FROM books WHERE id = ?", (book_id,))   # right
conn.execute("SELECT * FROM books WHERE id = ?", (book_id))    # wrong: not a tuple
```

## All or nothing: `with conn:`

When several changes must happen together:

```python
with conn:
    conn.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("Emma", 1815))
    conn.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("Dune", 1))
```

`with conn:` commits if the block finishes without an error, and **rolls
back** if one happens. We measured: the second row hit `UNIQUE` and `Emma`
wasn't added either; only the earlier `Dune` remained in the table. Jobs
where "half done is a disaster", like a money transfer, are written like
this. (`with conn:` doesn't **close** the connection; that's done in
`get_db`'s `finally`.)

## How many rows?

```python
conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
```
