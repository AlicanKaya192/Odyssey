Kitap uç noktaları `routers/books.py`'ye taşınmış ama iki şey eksik.

**Yapman gerekenler:**

1. `routers/books.py`: router'a `prefix="/books"` ve `tags=["books"]` ver.
2. `main.py`: router'ı uygulamaya ekle.

- `GET /books` → `{"1": "Dune", "2": "Emma"}`
- `GET /books/2` → `{"id": 2, "title": "Emma"}`
- `GET /books/9` → `404`
