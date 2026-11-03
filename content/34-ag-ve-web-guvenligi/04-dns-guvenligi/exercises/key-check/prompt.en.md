The parent domain publishes the SHA-256 hash (hex text) of the child
domain's key. `key_ok(presented, published)` should hash the presented
key and compare it with the published one in **constant time**
(`hmac.compare_digest`), returning `True`/`False`.

**Expected output:**

```
True
False
```
