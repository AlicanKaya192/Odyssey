A one-number RNN: `h_0 = 0`, `h_t = tanh(w · h_{t-1} + x_t)`.
`gradient_through_time(w, xs)` should return the derivative of the last state
with respect to the earlier states: first `1.0` (with respect to itself),
then walking back, multiplying the previous one by `w · (1 − h_t²)` at every
step, down to `h_0`. 4 places.

**Expected output:**

```
[1.0, 0.496, 0.24, 0.1041, 0.0219]
[1.0, 0.1721, 0.0344, 0.0119, 0.01]
```
