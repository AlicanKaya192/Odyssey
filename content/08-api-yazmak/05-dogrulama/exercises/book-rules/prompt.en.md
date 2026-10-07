**What to do:** put rules on the `Book` model's fields and have
`POST /books` return the book as it is with `201`.

| Field | Rule |
|---|---|
| `title` | 1–80 characters |
| `year` | 1450–2100 (both included) |
| `pages` | greater than 0 |

- `{"title": "Dune", "year": 1965, "pages": 412}` → `201`
- `{"title": "", "year": 1965, "pages": 412}` → `422`
- `{"title": "Dune", "year": 2101, "pages": 412}` → `422`
- `{"title": "Dune", "year": 1450, "pages": 1}` → `201`
- `{"title": "Dune", "year": 1965, "pages": 0}` → `422`
