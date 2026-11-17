`clip_by_norm(grads, max_norm)` gets each parameter's gradient as a list of
numbers. The square root of the sum of the squares of all the numbers is the
total norm. If the norm exceeds `max_norm`, multiply every number by
`max_norm / norm`; otherwise leave them. Return `[norm, clipped lists]` with
numbers at 4 places.

**Expected output:**

```
[5.0, [[0.6, 0.8]]]
[3.0, [[1.0], [2.0, 2.0]]]
```
