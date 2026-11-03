`check(expected, sent)` should compare the token on the server
(`expected`) with the token from the form (`sent`). Return `True` if both
are non-empty texts and equal, and `False` otherwise. Compare with
`hmac.compare_digest`. The starter code uses `==` and counts two empty
values as equal.

**Expected output:**

```
True
False
False
False
```
