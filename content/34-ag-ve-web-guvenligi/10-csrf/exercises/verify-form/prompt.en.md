`sessions` is a session ID → CSRF token dictionary. `verify(sessions,
sid, form)` should return `"ok"` if the session has a token and the
form's `"csrf"` value matches it with `hmac.compare_digest`, and
`"rejected"` otherwise. If the form has no token or the session is
unknown, `"rejected"` too.

**Expected output:**

```
ok
rejected
rejected
rejected
```
