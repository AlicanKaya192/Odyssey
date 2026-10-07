What the type you write on a path parameter accepts and what it rejects
with `422` (measured).

| Type | Accepts | Rejects | `type` |
|---|---|---|---|
| `int` | `/books/2` → `2` | `abc`, `2.5` | `int_parsing` |
| `float` | `/price/3` → `3.0`, `/price/1.5` → `1.5` | `abc` | `float_parsing` |
| `str` | Anything (`%20` becomes a space) | — | — |
| `bool` | `1`, `true`, `yes`, `on` → `true`; `0`, `false`, `no`, `off` → `false` | `maybe` | `bool_parsing` |

## The parts of a 422 body

```json
{"detail": [{
  "type": "float_parsing",
  "loc": ["path", "p"],
  "msg": "Input should be a valid number, unable to parse string as a number",
  "input": "abc"}]}
```

- `detail` is a **list**: if there are several errors, each is a separate
  item.
- The first item of `loc` says where it came from: `path` (the address),
  `query` (the query, Query Parameters section), `body` (the body, Request
  Bodies section).
- `msg` is an English explanation; `type` a short name for machines.

## A value that contains slashes

Normally a path parameter cannot contain `/`. For a value such as a file
path, the `:path` suffix:

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
```

`GET /files/docs/2024/report.txt` → `{"file_path": "docs/2024/report.txt"}`.

## Common mistakes

| Symptom | Cause |
|---|---|
| Every request `422` with `loc: ["query", "book_id"]` | There is no `{book_id}` in the address; FastAPI took the parameter for a query (write the same name in both places) |
| `/books/latest` → `422` | The path with a variable was written first; move the fixed path up |
| `/books/2` is not found | No type written; `"2"` is looked up as text |
| `500` for a missing record | A `KeyError` instead of `HTTPException(404)` |
