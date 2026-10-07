`PUT` ve `PATCH`'i veritabanıyla yazmak.

## `PUT`: bütün sütunlar

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

`rowcount` `0` ise kitap yoktu (ölçtük: olmayan numarada `UPDATE` →
`rowcount` `0`).

## `PATCH`: yalnızca gönderilen sütunlar

Kaç sütunun değişeceği isteğe göre değişiyor; `SET` kısmını kurmak
gerekiyor:

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

`{"year": 1966}` → `UPDATE books SET year = ? WHERE id = ?`, değerler
`(1966, 1)` (ölçtük).

**Bu birleştirme neden güvenli?** Sorgu metnine giren yalnızca **sütun
adları** (`year`), ve onlar kullanıcıdan değil `BookPatch` modelinin
alanlarından geliyor: modelde olmayan bir alan zaten atılıyor. Değerler
yine `?` ile. Kural aynı: kullanıcının yazdığı **değer** sorgu metnine
girmez.

## Sonra okumak

`UPDATE` güncel satırı döndürmüyor; cevabı vermek için bir `SELECT` daha
gerekiyor. Gövde boşsa (`{}`) hiçbir şey güncellenmiyor ama kayıt yine
okunup döndürülüyor (ya da yoksa `404`).
