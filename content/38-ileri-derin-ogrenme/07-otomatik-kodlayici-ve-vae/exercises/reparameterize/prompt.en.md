`reparameterize(mu, logvar, eps)` should compute the VAE's code:
`z = mu + exp(0.5 · logvar) · eps`. The random numbers are given ready as
`eps`. Return the result as a list with 3 places.

**Expected output:**

```
[1.0, 0.0]
[2.5]
```
