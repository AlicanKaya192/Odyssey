| Term | Meaning |
|---|---|
| **GAN** (generative adversarial network) | A generative model made of a generator and a discriminator trained against each other |
| **Generator** (G) | The network that produces samples from random noise; it never sees real data |
| **Discriminator** (D) | A binary classifier that gives the probability that a sample is real |
| **Adversarial loss** | A measure of how well the generator fools the discriminator; in practice $-\log D(G(z))$ |
| **Equilibrium** | The state where the discriminator cannot tell real from fake and says 0.5 to everything |
| **Best discriminator** | $D^*(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_G(x)}$ |
| **Mode** | A peak of the distribution; in the section one of the eight clusters on the ring |
| **Mode collapse** | The generator producing only part of the data and forgetting the rest |
| **Logit** | The discriminator's raw output before the `sigmoid` |

**Keep in mind:**

- The two networks are trained in turn: first the discriminator (a real and a
  fake batch), then the generator (a new fake batch, with the gradient passing
  through the discriminator).
- The old generator loss $\log(1 - D(G(z)))$ has an almost zero gradient
  early on ($-0.01$ at $p = 0.01$); that of $-\log D(G(z))$ is $-0.99$.
- The loss shows mode collapse only indirectly; look at the generated samples.
