Both endpoints are written but one never runs:

- `GET /books/latest` → `422` (expected: the newest book)

**What to do:** find the cause and fix it. The right state:

- `GET /books/latest` → `{"id": 1, "title": "Dune", "year": 1965}`
- `GET /books/3` → `{"id": 3, "title": "Ulysses", "year": 1922}`
