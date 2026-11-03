The cookie has the form `value.tag`; the tag is the HMAC-SHA256 hex
digest of the value with `key`. `read_cookie(cookie, key)` should split at
the **last** dot, recompute the tag and compare it with
`hmac.compare_digest`; return the value if it matches, and `None` if it
does not or there is no dot. `key` is text (`encode()`).

**Expected output:**

```
user=ada
None
None
```
