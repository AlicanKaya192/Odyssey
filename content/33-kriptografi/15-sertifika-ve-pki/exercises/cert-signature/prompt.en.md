`digest` is ready. `check_signature(cert, e, n)` should verify the
certificate's signature with the CA's public key. The signed bytes are
`json.dumps(..., sort_keys=True).encode()` of the fields **other than
`signature`**. The starter code also puts the signature itself into the
signed data and rejects a genuine certificate.

**Expected output:**

```
True
False
```
