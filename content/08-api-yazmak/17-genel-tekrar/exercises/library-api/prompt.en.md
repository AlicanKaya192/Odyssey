A library API from scratch.

| Request | Answer |
|---|---|
| `POST /books` | `201`, the book + `id` |
| `GET /books?year=...` | a list (the filter is optional) |
| `GET /books/{id}` | the book or `404` |
| `PATCH /books/{id}` | only the sent fields change |
| `DELETE /books/{id}` | `204` |

- `title` at least 1 character, `year` 1450–2100 (both in `PATCH` too).
- `id` starts at 1 and never repeats, even after a deletion.
- Not found: `404`, `"Book not found"`.
