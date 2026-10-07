Not every endpoint returns JSON: `/status` is plain text. You will write a
function that reads the body according to its type.

**What to do:**

1. Write the function `read_body(path)`: it sends the request; if the
   `Content-Type` header starts with `application/json` it returns
   `response.json()`, otherwise `response.text`.
2. Read three addresses; for each print the address, the name of the
   returned value's type (`type(...).__name__`) and the value.

**Expected output:**

```
/status str ok
/authors/2 dict {'id': 2, 'name': 'Herbert', 'country': 'US', 'born': 1920}
/authors dict 8 authors
```
