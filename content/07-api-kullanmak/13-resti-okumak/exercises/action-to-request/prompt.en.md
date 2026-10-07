Write REST's contract as a function: given a job name and an optional
identifier, it returns the right method and address.

**What to do:** the function `to_request(action, book_id)` returns a
`(method, address)` **tuple**:

| `action` | Method | Address |
|---|---|---|
| `"list"` | `GET` | `/books` |
| `"read"` | `GET` | `/books/<id>` |
| `"create"` | `POST` | `/books` |
| `"replace"` | `PUT` | `/books/<id>` |
| `"change"` | `PATCH` | `/books/<id>` |
| `"remove"` | `DELETE` | `/books/<id>` |

For `list` and `create`, `book_id` comes in as `None`. Then print the method
and address for every job in the `jobs` list.

**Expected output:**

```
list -> GET /books
read -> GET /books/42
create -> POST /books
change -> PATCH /books/7
remove -> DELETE /books/3
replace -> PUT /books/9
```
