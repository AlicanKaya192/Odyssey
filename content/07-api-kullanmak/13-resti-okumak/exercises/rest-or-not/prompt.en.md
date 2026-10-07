Write a function that checks an endpoint against REST's rule about verbs.
There are no requests here.

**What to do:** write the function `check_endpoint(method, path)`:

1. Split the path into pieces at `/` (drop empty pieces). If any piece,
   lower-cased, **starts with** one of the words `get`, `create`, `update`,
   `delete`, `remove`, `add`, return `"verb in path"`.
2. Otherwise return `"ok"`.

In short: **a verb in the address** gives `"verb in path"`, otherwise
`"ok"`. Then print the result for every endpoint in the `endpoints` list.

**Expected output:**

```
GET /books -> ok
GET /getBooks -> verb in path
POST /books/42/delete -> verb in path
DELETE /books/42 -> ok
POST /createBook -> verb in path
GET /authors/6/books -> ok
PATCH /books/42 -> ok
```
