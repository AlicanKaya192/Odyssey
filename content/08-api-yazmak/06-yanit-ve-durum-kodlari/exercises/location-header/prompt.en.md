The `Book` model and the empty `books` dictionary are ready.

**What to do:**

1. `POST /books`: put the book in `books[new_id]` (ids start at 1), return
   `{"id": ..., "title": ..., "year": ...}` with `201`, and add the header
   `Location: /books/<id>` to the answer.
2. `GET /books/{book_id}`: return the book.

- `POST /books`, `{"title": "Dune", "year": 1965}` → `201`, header `location: /books/1`
- `GET /books/1` → `{"title": "Dune", "year": 1965}`
