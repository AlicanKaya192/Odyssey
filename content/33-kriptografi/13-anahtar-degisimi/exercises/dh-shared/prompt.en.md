`dh_shared(their_public, my_secret, p)` computes the shared secret but
never checks what came from the other side. If `1 < their_public < p - 1`
does not hold, it should return `"invalid"`; if it is valid, `pow(
their_public, my_secret, p)`. If the public value is `1` or `p - 1`, the
shared secret can only be `1` or `p - 1`, so it can be guessed.

**Expected output:**

```
2
invalid
invalid
```
