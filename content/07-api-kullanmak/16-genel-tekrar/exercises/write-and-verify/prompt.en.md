A review of Sections 08 and 09: writing with an identity and verifying the
result.

**What to do:**

1. Get the token with `os.environ.get("LIBRARY_TOKEN", "letmein")` and add it
   to a session as the `Authorization` header.
2. Add the book `{"title": "The Word for World Is Forest", "price": 11.5, "author_id": 6}`;
   print the code and the `Location`.
3. Set the price to `9.99` with a `PATCH` to the address in `Location`.
4. Read the same address with `GET` and print the title, author and price.

**Expected output:**

```
created: 201 /books/24
patched: 200
The Word for World Is Forest Le Guin 9.99
```
