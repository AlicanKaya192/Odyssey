In the module's first sections we saw four generative models. The numbers
come from the measurements in the sections; the data and settings are small,
so the results belong to these experiments.

| | Autoencoder | VAE | GAN | Diffusion |
|---|---|---|---|---|
| What it learns | To compress and rebuild | The code as a distribution | To fool the discriminator | To predict the added noise |
| Training | One network, reconstruction error | One network, reconstruction + KL | A game of two networks | One network, ordinary regression |
| Where a new sample comes from | Unclear | The standard normal | Noise, in one pass | Noise, in 100 steps |
| Result in the section | Clear digit from a random code 32% | All 10 digits | 8 clusters; 8, 6, 6 at 0.01 | 8 clusters; 8, 8, 8 at 0.01 too |
| Strength | Compression, anomalies | An orderly latent space | Sharp samples, fast generation | Stable training, every kind |
| Weakness | Not a generator | Blurry | Fragile training, mode collapse | Slow generation |

**Which one when?**

- To **compress** data or find **anomalies**: the autoencoder.
- If you need an orderly **latent space** (interpolation, a small code inside
  another model): the VAE. In modern image generators the VAE is there for
  exactly this job.
- If **fast** generation matters and you can tune the training carefully: the
  GAN.
- If **quality and variety** matter and generation time is not a problem:
  diffusion. Most of today's image generators are diffusion models working in
  a VAE's latent space.

**Common mistakes:**

- **Dropping the fresh noise in the reverse step.** The samples gather in
  the middle of the clusters and the variety is lost (in the section the mean
  distance to the centre was 0.064, against 0.125 in the real data).
- **Not giving the step number to the network.** The same network runs at
  every step; if it does not know which step it is at, it cannot know how much
  noise to remove.
- **Using `alphas` instead of `alpha_bar`.** The one-step noise formula needs
  the cumulative product (`alpha_bar`); the reverse step uses both.
- **Looking at a single measure.** In the section the GAN led on closeness to
  the clusters, diffusion on stability; when judging a model look at both
  quality and variety.
