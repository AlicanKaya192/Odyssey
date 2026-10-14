| | Autoencoder | VAE |
|---|---|---|
| Code | A single point | A distribution ($\mu$, $\sigma$) |
| Loss | Reconstruction only | Reconstruction + β × KL |
| Where the codes sit | Up to the network (in the lesson mean −9.99, 1.69) | Close to the standard normal (mean ~0, spread ~1) |
| A new example | Unclear where to draw it from | From the standard normal |
| 1000 codes from the standard normal | 4 digits (3 and 5 with the other seeds) | 10 digits (with all three seeds) |
| Reconstruction, 8-number code | Better (0.0139) | Blurrier (0.025) |
| When | Compression, denoising, anomalies | Generation, an orderly latent space, interpolation |

**Common mistakes:**

- **Mixing up the KL's signs or order.** The formula is
  $\frac{1}{2}\sum(\mu^2 + \sigma^2 - \log\sigma^2 - 1)$; for the standard
  normal (`mu = 0`, `logvar = 0`) the result must be 0. Test your code with
  that first.
- **Taking `logvar` for the variance.** `std = np.exp(0.5 * logvar)`;
  `np.sqrt(logvar)` gives `nan` for a negative number.
- **Drawing a sample when measuring.** The test error then moves on every
  run; use $\mu$ for measuring.
- **Growing β blindly.** The latent space becomes orderly, but past a point
  the model collapses and turns everything into the same blob. If you see
  the KL drop to zero, β is too large.
- **Trusting a single seed.** In the lesson the judge's "sure" share changed
  from seed to seed; if the result matters, repeat the training with a few
  seeds.
