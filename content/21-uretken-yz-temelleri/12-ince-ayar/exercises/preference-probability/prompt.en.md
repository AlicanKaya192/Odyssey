`prefer_prob(r_a, r_b)` should return the probability that a is preferred to
b in the Bradley–Terry model: `1 / (1 + exp(-(r_a - r_b)))`, as a `float`
rounded to 3 places.

**Expected output:**

```
0.731
0.5
```
