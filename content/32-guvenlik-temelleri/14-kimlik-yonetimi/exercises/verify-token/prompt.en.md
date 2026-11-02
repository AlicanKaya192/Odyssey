The toy token has two parts: `body.signature`. The body is the base64url
encoding of JSON, the signature the HMAC-SHA256 hash (hex) of the body with
`key`. `make_token` is ready.

`verify_token(token, key)` should return:

- `"malformed"` if the number of dots is not 1,
- `"bad-signature"` if the signature does not match (with
  `hmac.compare_digest`),
- `"malformed"` if the body cannot be decoded,
- otherwise the dictionary of claims.

Check the signature **before decoding the body**.

**Expected output:**

```
{'sub': 'ada', 'role': 'user'}
bad-signature
bad-signature
malformed
```
