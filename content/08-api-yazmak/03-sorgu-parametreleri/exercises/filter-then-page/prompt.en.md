**What to do:** `GET /books` both filters and pages:

- `author` is optional (no filter if missing), `page` defaults to `1`,
  `per_page` to `2`.
- The answer: `{"total": ..., "titles": [...]}`. `total` is the length of the
  **filtered** list; `titles` are the titles of the books on that page.

- `GET /books?author=Austen` → `{"total": 2, "titles": ["Emma", "Persuasion"]}`
- `GET /books?author=Austen&page=2` → `{"total": 2, "titles": []}`
- `GET /books?page=2` → `{"total": 6, "titles": ["Ulysses", "Kindred"]}`
- `GET /books?author=Nobody` → `{"total": 0, "titles": []}`
