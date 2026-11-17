`accumulated(value, times)` should build `y = x²` `times` times and call
`backward()` each time, **without** zeroing the gradient in between. At the end it
should return the number in `x.grad`. Why is the result `times · 2x`?

**Expected output:**

```
12.0
-6.0
```
