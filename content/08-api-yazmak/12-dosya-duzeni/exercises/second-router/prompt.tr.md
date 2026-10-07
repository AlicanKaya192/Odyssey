`routers/books.py` hazır ve uygulamaya eklenmiş.

**Yapman gerekenler:**

1. `routers/authors.py`: `prefix="/authors"` ile bir router;
   `authors = {1: "Frank Herbert", 2: "Jane Austen"}`.
   - `GET /authors` → sözlük
   - `GET /authors/{author_id}` → `{"id": ..., "name": ...}`; yoksa `404`
     (`"Author not found"`)
2. `main.py`: yeni router'ı da ekle.

- `GET /authors/2` → `{"id": 2, "name": "Jane Austen"}`
- `GET /books/1` hâlâ çalışıyor
