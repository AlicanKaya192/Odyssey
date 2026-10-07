The `books` dictionary is ready.

**What to do:**

1. A `get_book(book_id)` dependency: `404` (`"Book not found"`) if the book is
   missing, otherwise it returns the book.
2. `GET /books/{book_id}` → the book.
3. `GET /books/{book_id}/age?now=2026` → `{"title": ..., "age": now - year}`
   (`now` defaults to `2026`).

Both endpoints get the book **from the dependency**; no `if` inside them.

- `GET /books/1/age` → `{"title": "Dune", "age": 61}`
- `GET /books/2/age?now=2000` → `{"title": "Emma", "age": 185}`
- `GET /books/9/age` → `404`
