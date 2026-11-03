`digest` is ready. `sign(message, d, n)` should sign the message's hash
with the **private exponent** `d`: `pow(hash, d, n)`. The starter code uses
the public exponent 65537; "signing" with the public key is something
anyone could do, and it does not pass verification.

**Expected output:**

```
True
```
