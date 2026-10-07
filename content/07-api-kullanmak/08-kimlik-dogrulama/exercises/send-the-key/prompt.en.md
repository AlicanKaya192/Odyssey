The `/stats` endpoint answers no one without a key. Try without it first, then
send the key in a header.

The key (the practice server's public reader key): `demo-key-123`, header
name `X-API-Key`.

**What to do:**

1. Send a request to `/stats` without a key and print the status code.
2. Send the same request with the key using `headers=`; print the status
   code, the number of books and the year of the newest book.

**Expected output:**

```
without key: 401
with key: 200
books: 23
newest: 1986
```
