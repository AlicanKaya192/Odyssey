| Term | Meaning |
|---|---|
| **VAE** (variational autoencoder) | An autoencoder that learns the code as a distribution instead of a point and pulls the latent space towards the standard normal |
| **Mean** $\mu$ | The centre of an image's code distribution |
| **Log-variance** $\log\sigma^2$ | The logarithm of the code distribution's spread; $\sigma = e^{\frac{1}{2}\log\sigma^2}$ |
| **Reparameterization trick** | Drawing the sample as $z = \mu + \sigma\varepsilon$; the randomness moves into $\varepsilon$ and the gradient reaches $\mu$ and $\sigma$ |
| **Prior** | The distribution the codes should resemble; here the standard normal |
| **KL divergence** | A measure of the difference between two distributions; for normal distributions $\frac{1}{2}\sum(\mu^2 + \sigma^2 - \log\sigma^2 - 1)$ |
| **Binary cross-entropy** | The reconstruction loss for pixels between 0 and 1; with a `sigmoid` output its derivative is `out - x` |
| **β** (KL weight) | The KL term's multiplier in the loss; the balance between reconstruction and an orderly latent space |
| **Posterior collapse** | The codes sticking to the standard normal and carrying no information about the image |
| **Interpolation** | Moving along the line between two codes and decoding every point |

**Keep in mind:**

- In a VAE the code distribution is known: a new example is drawn from the
  standard normal. In the lesson the autoencoder produced 4 of the 10 digits
  from there, the VAE all of them.
- `beta = 0` is an ordinary autoencoder; with a very large β the model
  collapses (at β = 4 the KL is 0, a single digit).
- When measuring, the centre of the code ($\mu$) is used; a sample is drawn
  only in training and generation.
