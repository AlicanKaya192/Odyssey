| Term | Meaning |
|---|---|
| **Diffusion model** | A model that learns the reverse of adding noise to data step by step and generates samples from pure noise step by step |
| **Forward process** | Adding a little noise to the data at every step; no model needed |
| **Reverse process** | Removing a little noise at every step using the network's noise prediction |
| **Noise schedule** | Each step's share of noise $\beta_t$; in the section linear from 0.0001 to 0.1 |
| $\bar\alpha_t$ | $\alpha_1 \cdots \alpha_t$ ($\alpha_t = 1 - \beta_t$); the share of the data left after $t$ steps |
| **Noise in one step** | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \varepsilon$ |
| **Time embedding** | Giving the step number to the network as sines and cosines |
| **Noise prediction** $\hat\varepsilon$ | The network's guess of the noise added to a point |
| **Latent diffusion** | Running diffusion in a VAE's small latent space |
| **Conditional generation** | Also giving the network a label or a text embedding to steer generation |

**Keep in mind:**

- Training is an ordinary mean-squared-error regression of a single network:
  the target is the added noise.
- In the reverse step fresh noise is added, except at the last step;
  without it the samples gather in the middle of the clusters and the variety
  is lost.
- In the section, even at the learning rate that broke the GAN (0.01), all
  eight clusters were found with three seeds. The price: the network runs 100
  times for one sample, once for a GAN.
