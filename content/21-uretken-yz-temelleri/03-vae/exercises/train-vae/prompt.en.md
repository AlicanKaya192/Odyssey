The starter code trains the lesson's VAE (`encode` and `decode` from the
read-only `vae_model.py`), but the two gradients into the encoder are empty.
Write:

- `d_mu = d_z + beta * mu / n`
- `d_lv = d_z * eps * 0.5 * std + beta * 0.5 * (std ** 2 - 1) / n`

The first part is the gradient from the sampling step, the second the KL's
gradient. `train(beta, steps)` returns the test images' error and the KL as
two `float`s rounded to 3 places.

**Expected output:**

```
[0.044, 2.012]
[0.047, 59.204]
```
