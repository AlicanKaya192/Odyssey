`gan_losses(p_real, p_fake)` should take the lists of probabilities the
discriminator gives the real and fake samples and return three means:
`[discriminator loss, generator loss, old generator loss]`. The
discriminator loss is `-(log(p_real) + log(1 - p_fake))` (the sum of the two
lists' means), the generator loss `-log(p_fake)`, the old form
`log(1 - p_fake)`. Every number a `float` rounded to 4 places.

**Expected output:**

```
[0.3953, 1.7533, -0.231]
[1.3863, 0.6931, -0.6931]
```
