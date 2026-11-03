`record` is a reset record (`hash`, `expires`, `used`) or `None`.
`status(record, token, now)` should check these **in this order** and
return: `"invalid"` if there is no record; `"used"` if it was used;
`"expired"` if `now >= expires`; `"invalid"` if the token's SHA-256 hash
does not match with `hmac.compare_digest`; otherwise `"ok"`.

**Expected output:**

```
ok
invalid
expired
used
invalid
```
