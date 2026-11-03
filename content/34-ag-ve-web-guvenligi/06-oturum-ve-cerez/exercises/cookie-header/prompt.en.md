`cookie_header(name, value, max_age)` should return a `Set-Cookie`
value in this form (parts separated by `"; "`):
`name=value; Max-Age=N; Path=/; Secure; HttpOnly; SameSite=Lax`.

**Expected output:**

```
session=abc123
Max-Age=3600
Path=/
Secure
HttpOnly
SameSite=Lax
```
