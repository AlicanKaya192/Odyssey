**What to do:** take the `tag` values sent several times with the same name
as a list; return them in alphabetical order with their count.

- `GET /tags?tag=python&tag=api&tag=docker` → `{"tags": ["api", "docker", "python"], "count": 3}`
- `GET /tags` → `{"tags": [], "count": 0}`
