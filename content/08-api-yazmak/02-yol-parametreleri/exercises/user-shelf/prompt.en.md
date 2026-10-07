The `shelves` dictionary keeps the books each user has read.

**What to do:** `GET /users/{user_id}/books`:

- `GET /users/1/books` → `{"user_id": 1, "books": ["Dune", "Emma"], "count": 2}`
- `GET /users/2/books` → `{"user_id": 2, "books": [], "count": 0}`
- `GET /users/9/books` → `404`, `{"detail": "User not found"}`

An empty shelf is not an error: the user exists but has no books. `404` only
if the user does not exist.
