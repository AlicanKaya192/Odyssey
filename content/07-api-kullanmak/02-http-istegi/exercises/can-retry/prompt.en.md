The connection dropped and five requests got no response. Which ones can you
resend without a second thought?

Idempotent methods: `GET`, `HEAD`, `OPTIONS`, `PUT`, `DELETE`. Not `POST`
and `PATCH`.

**What to do:**

1. Write the function `can_retry(method)`: it returns `True` if the method is
   idempotent and `False` otherwise. The method may arrive in lower case
   (`"patch"`); turn it into upper case before comparing.
2. For every request in the `failed` list, write `retry` if it can be resent
   and `ask first` if not; then the method (in upper case) and the address.

**Expected output:**

```
retry GET /books
ask first POST /orders
retry DELETE /books/7
ask first PATCH /books/7
retry PUT /books/7
```
