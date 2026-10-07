Five methods, their decorators and what happens when each is repeated.

| Method | Decorator | Changes things? | Sent twice |
|---|---|---|---|
| `GET` | `@app.get` | No | The same answer (safe) |
| `POST` | `@app.post` | Yes | Two records may be created |
| `PUT` | `@app.put` | Yes | The same result (the whole record has the same value again) |
| `PATCH` | `@app.patch` | Yes | Usually the same |
| `DELETE` | `@app.delete` | Yes | The first deletes, the second gets `404` |

Methods whose result is the same when sent twice are called **idempotent**
(`GET`, `PUT`, `DELETE`). The retry rule in API 1 comes from here: a client
may send a request again; repeating a `POST` is risky, the others are not.

## The pattern

```python
@app.get("/items")
def list_items():
    ...


@app.post("/items")
def create_item():
    ...
```

- One address + one method = one function.
- Function names become summaries in the docs (`list_items` → "List Items").
- If the same address and method are written twice, the **first** wins; the
  second is never called. Watch out for this after copy and paste.

## Which code when (FastAPI by itself)

| Situation | Code |
|---|---|
| The endpoint ran | `200` |
| No such address | `404` |
| The address exists, the method does not | `405` |
| An extra `/` at the end | `307` → to the right address |
| An error inside the function | `500` |
