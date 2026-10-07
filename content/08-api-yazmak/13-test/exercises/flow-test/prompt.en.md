**What to do:** **one** test that tries a book's whole life:

1. `POST /books` → `201`; take the `id` from the answer.
2. `GET /books/{id}` → `200`, `{"title": ..., "year": ...}`.
3. `DELETE /books/{id}` → `204`.
4. `GET /books/{id}` → `404`.

In the broken versions deleting deletes nothing, reading returns an empty
body, or the number in the answer is wrong.
