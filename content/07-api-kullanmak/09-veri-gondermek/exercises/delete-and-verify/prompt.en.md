Sense and Sensibility (number 7) is leaving the library.

**What to do:**

1. Send `DELETE /books/7`; print the status code and whether the body is
   empty (`r.text == ""`).
2. Confirm the deletion with `GET /books/7`; print the status code.
3. Send the same delete once more; print the status code.

**Expected output:**

```
delete: 204 empty body: True
get after delete: 404
delete again: 404
```

The second delete has a different code but the same result: the book is
gone.
