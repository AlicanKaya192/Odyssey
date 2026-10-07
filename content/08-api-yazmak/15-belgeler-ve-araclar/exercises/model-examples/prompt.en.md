**What to do:**

1. A `Book` model: `title` (example `"Dune"`, description `The book's
   title`), `year` (example `1965`, description `Year of first
   publication`).
2. `POST /books` → `201`, return the book (`tags=["books"]`).
3. `GET /old-books` → `[]`; shown as **deprecated** in the docs.

The check looks at the `Book` schema and the `deprecated` field of
`/old-books` in `/openapi.json`.
