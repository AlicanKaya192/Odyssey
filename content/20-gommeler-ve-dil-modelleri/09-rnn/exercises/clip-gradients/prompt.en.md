`clip_gradients(grads, max_norm)` should compute the size of the derivatives
(the square root of the sum of squares). If the size exceeds `max_norm`,
multiply every derivative by `max_norm / size`; otherwise leave them as they
are. 3 places.

**Expected output:**

```
[3.0, 4.0]
[3.0, 4.0]
[0.0, 0.0]
```
