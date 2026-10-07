The `books` dictionary is ready.

**What to do:** `GET /books/{book_id}`:

- If the book exists, return it: `GET /books/2` → `{"id": 2, "title": "Emma", "year": 1815}`.
- Otherwise `404` and `{"detail": "Book not found"}`.
- `book_id` must be an integer: `GET /books/abc` → `422`.
