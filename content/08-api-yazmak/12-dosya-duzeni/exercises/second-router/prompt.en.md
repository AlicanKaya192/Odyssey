`routers/books.py` is ready and added to the application.

**What to do:**

1. `routers/authors.py`: a router with `prefix="/authors"`;
   `authors = {1: "Frank Herbert", 2: "Jane Austen"}`.
   - `GET /authors` → the dictionary
   - `GET /authors/{author_id}` → `{"id": ..., "name": ...}`; `404`
     (`"Author not found"`) if missing
2. `main.py`: add the new router too.

- `GET /authors/2` → `{"id": 2, "name": "Jane Austen"}`
- `GET /books/1` still works
