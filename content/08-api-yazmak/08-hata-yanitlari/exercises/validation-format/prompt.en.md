The endpoints are ready.

**What to do:** a handler that turns every validation error into one
format:

```json
{"error": "invalid_input",
 "fields": ["title", "year"]}
```

`fields`: each error's `loc` without its first item (`body`, `query`),
joined with dots.

- `POST /books` `{"title": "", "year": "x"}` → `422`, `fields` `["title", "year"]`
- `GET /books?limit=abc` → `422`, `fields` `["limit"]`
- `POST /books` `{"title": "Dune", "year": 1965}` → `201`
