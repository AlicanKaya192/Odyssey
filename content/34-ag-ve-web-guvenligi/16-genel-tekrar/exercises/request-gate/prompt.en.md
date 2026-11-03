Combine the CSRF and Secure APIs sections. `gate(req, sessions, notes)`
should return a status code:

- `401` if the cookie has no session,
- `403` on `POST` if `origin` is not in `ALLOWED_ORIGINS` or `csrf` does
  not match the session's (`compare_digest`),
- `404` if the note does not exist or its owner is not the session's
  user,
- otherwise `200`.

**Expected output:**

```
200
404
401
403
200
```
