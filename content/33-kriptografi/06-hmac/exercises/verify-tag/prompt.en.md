`make_tag` is ready. `verify_tag(key_hex, message, tag)` should
recompute the expected tag and compare it with the given `tag` in
**constant time** (`hmac.compare_digest`); return `True` if equal, `False`
otherwise. Do not use `==`.

**Expected output:**

```
True
False
False
```
