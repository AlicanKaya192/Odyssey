Sıfırdan bir kütüphane API'si.

| İstek | Cevap |
|---|---|
| `POST /books` | `201`, kitap + `id` |
| `GET /books?year=...` | liste (süzgeç isteğe bağlı) |
| `GET /books/{id}` | kitap ya da `404` |
| `PATCH /books/{id}` | yalnızca gönderilen alanlar değişir |
| `DELETE /books/{id}` | `204` |

- `title` en az 1 karakter, `year` 1450–2100 (ikisi de `PATCH`'te de).
- `id` 1'den başlar, silmeden sonra da tekrar etmez.
- Bulunamayan: `404`, `"Book not found"`.
