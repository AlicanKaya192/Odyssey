curl's most used options and their requests equivalents.

## Options

| curl | What it does | requests |
|---|---|---|
| `curl URL` | A GET request | `requests.get(URL)` |
| `-X POST` | Chooses the method | `requests.post(...)` |
| `-H "Name: value"` | Adds a header | `headers={"Name": "value"}` |
| `-d 'text'` | Sends a body (makes the method POST) | `data=` / `json=` |
| `--json '{...}'` | A JSON body + headers (newer curl) | `json={...}` |
| `-u name:password` | Basic authentication | `auth=("name", "password")` |
| `-i` | Shows the response headers too | `r.headers` |
| `-s` | Silent (no progress) | |
| `-o file` | Writes the response to a file | `open(...).write(r.content)` |
| `-G --data-urlencode "q=a b"` | Encodes a query parameter | `params={"q": "a b"}` |
| `--max-time 5` | A timeout | `timeout=5` |

## Examples

```text
curl -i https://api.example.com/books?author=Austen
curl -H "X-API-Key: abc" https://api.example.com/stats
curl -X PATCH --json @price.json -H "Authorization: Bearer abc" \
  https://api.example.com/books/2
curl -X DELETE https://api.example.com/books/7 -H "Authorization: Bearer abc"
```

## Watch out on Windows

- In PowerShell `curl` may point to a different command: write `curl.exe`.
- On the command line, double quotes inside JSON are escaped with a
  backslash: `-d "{\"a\": 1}"`. For long bodies sending from a file is easier:
  `-d @body.json`.
