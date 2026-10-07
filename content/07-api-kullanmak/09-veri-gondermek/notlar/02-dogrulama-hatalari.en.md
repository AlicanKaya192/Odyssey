Reading and fixing the error when the server rejects the data you sent.

## The practice server's rules

| Field | Rule | `detail` when broken |
|---|---|---|
| `title` | Non-empty text | `title must be a non-empty string` |
| `price` | A positive number | `price must be a positive number` |
| `author_id` | An existing author | `author_id does not exist` |
| body | A JSON object | `the body must be a JSON object` |

`title` and `price` are required with `POST` and `PUT`; with `PATCH` only
the fields you send are checked.

## Using the error response

```python
r = requests.post(BASE + "/books", json=new, headers=AUTH)
if r.status_code == 422:
    print("rejected:", r.json()["detail"])
elif r.status_code == 201:
    print("created:", r.headers["Location"])
else:
    print("unexpected:", r.status_code)
```

## Checking before sending

It is a good habit to check, on the client too, the errors that can be caught
before reaching the server; it cuts the number of requests and tells the user
sooner:

```python
def problems(book):
    found = []
    if not str(book.get("title", "")).strip():
        found.append("title is empty")
    if not isinstance(book.get("price"), (int, float)) or book["price"] <= 0:
        found.append("price must be positive")
    return found
```

But the server always has the last word: the check on the client **does not
replace** the server's check; it only comes before it.

## Common mistakes

- Sending the price as text: `{"price": "11.50"}` → not a number, rejected.
- Using `data=`: the body goes as a form, not JSON.
- Sending `PATCH` to the list address (`/books`): `405`; it needs the address
  of a single record (`/books/2`).
