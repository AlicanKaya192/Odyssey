`Book` modeli ve boş `books` sözlüğü hazır.

**Yapman gerekenler:**

1. `POST /books`: kitabı `books[yeni_id]`'ye koy (id 1'den başlar), `201`
   ile `{"id": ..., "title": ..., "year": ...}` döndür ve cevaba
   `Location: /books/<id>` başlığını ekle.
2. `GET /books/{book_id}`: kitabı döndür.

- `POST /books`, `{"title": "Dune", "year": 1965}` → `201`, başlık `location: /books/1`
- `GET /books/1` → `{"title": "Dune", "year": 1965}`
