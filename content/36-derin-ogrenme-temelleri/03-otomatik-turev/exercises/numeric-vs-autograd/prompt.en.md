`compare(value)` should return two derivatives of `f(t) = 3t² + t`: the
automatic one (with a `float64` tensor) and the numerical one with `h = 1e-4`,
`(f(x + h) − f(x − h)) / 2h`. Both with 4 places, `[automatic, numerical]`.

**Expected output:**

```
[10.0, 10.0]
[-11.0, -11.0]
```
