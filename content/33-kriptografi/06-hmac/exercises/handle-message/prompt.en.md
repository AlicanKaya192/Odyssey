`make_tag` is ready. `handle(key_hex, message, tag)` should verify the
tag **first** (`hmac.compare_digest`). If it does not match, return
`"rejected"` and never use the message; if it matches, return
`"accepted: " + message`.

**Expected output:**

```
accepted: ok
rejected
rejected
```
