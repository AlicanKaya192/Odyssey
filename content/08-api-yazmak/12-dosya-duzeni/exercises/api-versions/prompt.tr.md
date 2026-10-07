`/books` bir sözlük döndürüyor (`{"1": "Dune", ...}`). Yeni istemciler
liste istiyor, eskileri bozmamak gerekiyor.

**Yapman gerekenler:**

1. `routers/books_v2.py`: aynı `books` verisini (`from routers.books import
   books`) liste olarak döndüren bir router: `[{"id": 1, "title": "Dune"}, ...]`.
2. `main.py`: eski router `/v1` önekiyle, yenisi `/v2` önekiyle.

- `GET /v1/books` → `{"1": "Dune", "2": "Emma"}`
- `GET /v2/books` → `[{"id": 1, "title": "Dune"}, {"id": 2, "title": "Emma"}]`
- `GET /v1/books/1` → `{"id": 1, "title": "Dune"}`
- `GET /books` → `404`
