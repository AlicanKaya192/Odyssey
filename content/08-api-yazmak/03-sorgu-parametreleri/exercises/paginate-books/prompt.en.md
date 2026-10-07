**What to do:** `GET /books` gives a paged answer:

```json
{"page": 1, "per_page": 2, "total": 6,
 "items": [ ...two books... ]}
```

- `page` defaults to `1`, `per_page` to `2`.
- For page `p` the slice starts at `(p - 1) * per_page`.
- A page past the end is not an error: `items` is empty.

- `GET /books` → Dune, Emma
- `GET /books?page=3` → Persuasion, Beloved
- `GET /books?page=2&per_page=4` → Persuasion, Beloved
- `GET /books?page=9` → `items: []`
