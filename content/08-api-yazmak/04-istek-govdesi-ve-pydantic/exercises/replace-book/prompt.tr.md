`books` sözlüğü hazır.

**Yapman gerekenler:**

1. `Book` modeli: `title`, `year`.
2. `GET /books/{book_id}`: kitabı döndür, yoksa `404` (`"Book not found"`).
3. `PUT /books/{book_id}`: kitabın tamamını gövdeyle değiştir ve
   `{"id": ..., "title": ..., "year": ...}` döndür; kitap yoksa `404`.

- `PUT /books/2`, `{"title": "Persuasion", "year": 1817}` → `{"id": 2, "title": "Persuasion", "year": 1817}`
- `GET /books/2` → `{"title": "Persuasion", "year": 1817}`
- `PUT /books/9`, `{"title": "X", "year": 1}` → `404`
- `PUT /books/1`, `{"title": "Dune"}` → `422`
