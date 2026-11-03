`digest` is ready. `verify(message, signature, e, n)` should return
`True` if the signature is right: `pow(signature, e, n)` must equal the
message's hash. The starter code compares the signature directly with the
hash; it never uses the public exponent.

**Expected output:**

```
True
False
```
