The `books` list is ready.

**What to do:** `GET /books` takes an optional `year_from` filter:

- If given, the books whose year is `year_from` or later.
- If not, all six books.

- `GET /books?year_from=1950` → Dune, Kindred, Beloved
- `GET /books` → six books
