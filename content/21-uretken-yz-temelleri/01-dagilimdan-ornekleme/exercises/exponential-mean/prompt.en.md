`exponential_mean(rate, n, seed)` should produce `n` exponential waiting times
by inverse transform (`t = -log(1 - u) / rate`) and return their mean as a
`float` rounded to 3 places. The uniform numbers are
`np.random.default_rng(seed).random(n)`.

**Expected output:**

```
2.014
0.498
```
