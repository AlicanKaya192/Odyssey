Apply the "parse, then decide" principle from the HTTP and HTTPS, SSRF
and CORS sections. `fetch_allowed(url)` should split the address with
`urlsplit`. Return `True` if the scheme is `http` or `https`, the
`hostname` is in `ALLOWED_HOSTS` and the port is not written (`None`) or
is 80/443.

**Expected output:**

```
True
False
False
True
False
False
```
