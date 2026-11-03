An API request is a method, a path and a body. `sign_request(key_hex,
method, path, body)` should join these three parts one per line (with
`\n`) and return the HMAC-SHA256 tag as hex. The tag must change when any
part changes.

**Expected output:**

```
5f917ac08d569fdd
True
False
```
