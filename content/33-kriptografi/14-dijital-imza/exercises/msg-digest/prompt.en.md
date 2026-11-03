`digest(message, n)` should return the number to be signed for a message:
the bytes of the `sha256(message.encode())` hash are turned into a number in
`"big"` order and reduced mod `n`. The starter code uses the message's own
bytes without hashing; for long messages only the last bytes survive.

**Expected output:**

```
True
False
True
```
