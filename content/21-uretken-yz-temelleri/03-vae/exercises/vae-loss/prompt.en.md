`vae_loss(x, out, mu, logvar, beta)` should compute the loss of a group of
examples. `x` and `out` are pixel lists, `mu` and `logvar` code lists (each
row one example). The reconstruction term per example is the binary
cross-entropy summed over the pixels:
`-(x * log(out) + (1 - x) * log(1 - out))`; the KL term is summed over the
dimensions too. Return `[mean reconstruction, mean KL,
reconstruction + beta * KL]`, the means over the examples, every number a
`float` rounded to 4 places.

**Expected output:**

```
[0.7623, 1.4417, 2.2039]
[0.7623, 1.4417, 1.4831]
```
