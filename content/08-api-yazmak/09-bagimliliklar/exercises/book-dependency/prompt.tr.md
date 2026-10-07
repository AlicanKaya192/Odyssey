`books` sözlüğü hazır.

**Yapman gerekenler:**

1. `get_book(book_id)` bağımlılığı: kitap yoksa `404`
   (`"Book not found"`), varsa kitabı döndürsün.
2. `GET /books/{book_id}` → kitap.
3. `GET /books/{book_id}/age?now=2026` → `{"title": ..., "age": now - year}`
   (`now` varsayılan `2026`).

İki uç nokta da kitabı **bağımlılıktan** alsın; içlerinde `if` olmasın.

- `GET /books/1/age` → `{"title": "Dune", "age": 61}`
- `GET /books/2/age?now=2000` → `{"title": "Emma", "age": 185}`
- `GET /books/9/age` → `404`
