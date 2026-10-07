Bir rehber API'si: her şeyi sen yazıyorsun.

| İstek | Cevap |
|---|---|
| `POST /contacts` | `201`, kişi + `id` |
| `GET /contacts` | liste |
| `GET /contacts/{id}` | kişi ya da `404` |
| `PATCH /contacts/{id}` | güncel kişi |
| `DELETE /contacts/{id}` | `204` |

- `name` en az 1, `phone` en az 3 karakter; `id` 1'den başlar ve tekrar
  etmez.
- Bulunamayanda `404`, `"Contact not found"`.

- `POST /contacts` `{"name": "Ada", "phone": "555-0101"}` → `{"name": "Ada", "phone": "555-0101", "id": 1}`
- `PATCH /contacts/1` `{"phone": "555-0199"}` → numara değişti, ad aynı
