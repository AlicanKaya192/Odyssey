**What to do:** an endpoint that returns the search word and its length.
`q` is required (no default).

- `GET /search?q=dune` → `{"q": "dune", "length": 4}`
- `GET /search` → `422`
