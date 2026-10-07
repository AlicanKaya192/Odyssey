The book endpoints have been moved to `routers/books.py`, but two things
are missing.

**What to do:**

1. `routers/books.py`: give the router `prefix="/books"` and `tags=["books"]`.
2. `main.py`: add the router to the application.

- `GET /books` → `{"1": "Dune", "2": "Emma"}`
- `GET /books/2` → `{"id": 2, "title": "Emma"}`
- `GET /books/9` → `404`
