Write a small client class for the library API. Each method sends a request
according to the REST contract.

**What to do:** write the `LibraryClient` class:

- `__init__(self, base, token)`: sets up a `requests.Session` and adds the
  `Authorization: Bearer <token>` header.
- `create(self, book)`: `POST /books`; returns the new book's **identifier**.
- `change(self, book_id, fields)`: `PATCH /books/<id>`; returns the updated
  book (a dictionary).
- `read(self, book_id)`: `GET /books/<id>`; returns the book, or `None` if
  missing.
- `remove(self, book_id)`: `DELETE /books/<id>`; returns the status code.

Then use the client to create a book, change its price, read it, delete it
and read it again; print each step as below.

**Expected output:**

```
created: 24
changed price: 9.0
read: Kindred 9.0
remove: 204
read after remove: None
```
