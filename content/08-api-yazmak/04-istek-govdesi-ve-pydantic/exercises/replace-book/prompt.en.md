The `books` dictionary is ready.

**What to do:**

1. A `Book` model: `title`, `year`.
2. `GET /books/{book_id}`: return the book, or `404` (`"Book not found"`).
3. `PUT /books/{book_id}`: replace the whole book with the body and return
   `{"id": ..., "title": ..., "year": ...}`; `404` if the book is missing.

- `PUT /books/2`, `{"title": "Persuasion", "year": 1817}` → `{"id": 2, "title": "Persuasion", "year": 1817}`
- `GET /books/2` → `{"title": "Persuasion", "year": 1817}`
- `PUT /books/9`, `{"title": "X", "year": 1}` → `404`
- `PUT /books/1`, `{"title": "Dune"}` → `422`
