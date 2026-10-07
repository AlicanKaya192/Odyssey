Writing `PUT` and `PATCH` with a database.

## `PUT`: every column

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookIn, db: DB):
    cur = db.execute("UPDATE books SET title = ?, year = ? WHERE id = ?",
                     (book.title, book.year, book_id))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, **book.model_dump()}
```

If `rowcount` is `0`, the book didn't exist (we measured: an `UPDATE` on a
missing number → `rowcount` `0`).

## `PATCH`: only the sent columns

How many columns change depends on the request; the `SET` part has to be
built:

```python
@app.patch("/books/{book_id}")
def update_book(book_id: int, patch: BookPatch, db: DB):
    changes = patch.model_dump(exclude_unset=True)
    if changes:
        sets = ", ".join(f"{name} = ?" for name in changes)
        cur = db.execute(f"UPDATE books SET {sets} WHERE id = ?",
                         (*changes.values(), book_id))
        db.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
    row = db.execute("SELECT id, title, year FROM books WHERE id = ?",
                     (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)
```

`{"year": 1966}` → `UPDATE books SET year = ? WHERE id = ?`, values
`(1966, 1)` (we measured).

**Why is this joining safe?** The only things that go into the query text
are **column names** (`year`), and they come not from the user but from the
`BookPatch` model's fields: a field not in the model is dropped anyway. The
values still go with `?`. The rule is the same: a **value** the user typed
never goes into the query text.

## Reading afterwards

`UPDATE` doesn't return the current row; giving the answer needs one more
`SELECT`. If the body is empty (`{}`), nothing is updated, but the record is
still read and returned (or `404` if it's missing).
