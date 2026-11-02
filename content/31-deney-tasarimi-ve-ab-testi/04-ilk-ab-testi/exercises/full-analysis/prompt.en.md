A test with 20,000 people (`make_experiment(n=20000, seed=743, lift=0.15)`).
One per line: the SRM p (3 places), the 95% interval of B − A (4 places)
and the result of `decide(srm_p, low, 0.003)`.

**Expected output:**

```text
0.026
0.0133 0.0317
ship
```
