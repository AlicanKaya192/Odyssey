The starter code has no generator: the fake samples always come from a
single cluster (around `CENTRES[0]`). The discriminator's step is missing
from the loop in `train_discriminator(steps)`. The real batch's gradient is
`backward(acts_r, (p_r - 1) / 128, disc)`, the fake batch's
`backward(acts_f, p_f / 128, disc)`; call `opt.step(disc, ...)` with their
layer-by-layer sum. After training the function returns the mean
probability the discriminator gives the real and fake samples. The network
pieces are in the read-only `gan_model.py`.

**Expected output:**

```
[0.87, 0.11]
```
