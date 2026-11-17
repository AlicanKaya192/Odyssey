`path(momentum)` should start from `w = 0` and shrink `(w − 3)²` with
`SGD(lr=0.1, momentum=...)` for 4 steps, appending `w` (4 places) to a list after
each step. See how `w` overshoots 3 with momentum.

**Expected output:**

```
[0.6, 1.08, 1.464, 1.7712]
[0.6, 1.62, 2.814, 3.9258]
```
