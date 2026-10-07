`books` sözlüğü hazır.

**Yapman gereken:** `GET /books/{book_id}`:

- Kitap varsa onu döndürsün: `GET /books/2` → `{"id": 2, "title": "Emma", "year": 1815}`.
- Yoksa `404` ve `{"detail": "Book not found"}`.
- `book_id` tam sayı olsun: `GET /books/abc` → `422`.
