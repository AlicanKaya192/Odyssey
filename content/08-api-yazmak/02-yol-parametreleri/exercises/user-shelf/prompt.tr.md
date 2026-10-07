`shelves` sözlüğü her kullanıcının okuduğu kitapları tutuyor.

**Yapman gereken:** `GET /users/{user_id}/books`:

- `GET /users/1/books` → `{"user_id": 1, "books": ["Dune", "Emma"], "count": 2}`
- `GET /users/2/books` → `{"user_id": 2, "books": [], "count": 0}`
- `GET /users/9/books` → `404`, `{"detail": "User not found"}`

Boş raf bir hata değil: kullanıcı var, kitabı yok. `404` yalnızca
kullanıcı yoksa.
