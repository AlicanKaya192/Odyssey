`gan_param_count(z_dim, hidden)` should build the lesson's two networks: the
generator `z_dim → hidden → 1` (ReLU in between), the discriminator
`1 → hidden → 1` (`LeakyReLU(0.2)` in between). Return the two networks'
parameter counts as a list `[generator, discriminator]`.

**Expected output:**

```
[97, 49]
[33, 25]
```
