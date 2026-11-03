`make_tag(key_hex, message)` should take the key (`bytes.fromhex`) and
the message (`encode()`) and return the HMAC-SHA256 tag as hex text.
`hmac.new(key, message_bytes, hashlib.sha256).hexdigest()`.

**Expected output:**

```
dd4da5ef5798f927
64
True
```
