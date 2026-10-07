The errors FastAPI gives without you writing them; all measured.

| Situation | Code | Body |
|---|---|---|
| The address doesn't exist (`GET /nothing`) | `404` | `{"detail": "Not Found"}` |
| The address exists, the method doesn't (`DELETE /items/pen`) | `405` | `{"detail": "Method Not Allowed"}` |
| A parameter/body doesn't fit the template | `422` | `{"detail": [{"type", "loc", "msg", "input"}]}` |
| An uncaught error in your code (`1 / 0`) | `500` | Plain text `Internal Server Error` |

## Don't confuse it with your own `404`

`GET /nothing` → `{"detail": "Not Found"}` (no such address).
`GET /items/xyz` → `{"detail": "Item not found"}` (the address exists, the
record doesn't).

Both are `404`. The client tells them apart by `detail`; that's why your own
message should say what wasn't found (`"Item not found"`, `"User not
found"`).

## Reading the `422` body

```json
{"detail": [{"type": "int_parsing", "loc": ["query", "x"],
             "msg": "Input should be a valid integer, ...", "input": "abc"}]}
```

| Field | Meaning |
|---|---|
| `type` | The kind of error (for machines) |
| `loc` | Where: `["query", "x"]`, `["body", "year"]` |
| `msg` | An explanation (for people) |
| `input` | The value that came in |

## When there's a `500`

The client only sees `Internal Server Error`. The real information is in
the server's terminal (or log): which file, which line, which error. In
Odyssey, when you try the exercise with **Run**, the terminal also writes
which line of which file the error came from.
