An address book API: you write all of it.

| Request | Answer |
|---|---|
| `POST /contacts` | `201`, the contact + `id` |
| `GET /contacts` | the list |
| `GET /contacts/{id}` | the contact or `404` |
| `PATCH /contacts/{id}` | the current contact |
| `DELETE /contacts/{id}` | `204` |

- `name` at least 1, `phone` at least 3 characters; `id` starts at 1 and
  never repeats.
- `404` when not found, `"Contact not found"`.

- `POST /contacts` `{"name": "Ada", "phone": "555-0101"}` → `{"name": "Ada", "phone": "555-0101", "id": 1}`
- `PATCH /contacts/1` `{"phone": "555-0199"}` → the number changed, the name is the same
