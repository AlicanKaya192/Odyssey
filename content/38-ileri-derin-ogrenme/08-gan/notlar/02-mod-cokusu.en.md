To fool the discriminator the generator does not have to learn the **whole**
distribution. If the data has two clusters (say around -2 and 2), imitating
only one of them very well also fools the discriminator for a while. This is
called **mode collapse**: the generated examples are realistic but always of
the same kind. The loss does not show it; you have to look at the examples.

## Counting the clusters

A small measure is enough: assign every generated example to its nearest
cluster centre and compute each centre's share. Below we build two sets of
examples by hand, one healthy and one collapsed:

```python
import torch


def mode_share(samples, centers):
    nearest = (samples - torch.tensor(centers)).abs().argmin(dim=1)
    counts = torch.bincount(nearest, minlength=len(centers)).float()
    return (counts / len(samples)).tolist()


gen = torch.Generator().manual_seed(0)
left = -2 + 0.3 * torch.randn(500, 1, generator=gen)
right = 2 + 0.3 * torch.randn(500, 1, generator=gen)
healthy = torch.cat([left, right])
collapsed = 2 + 0.3 * torch.randn(1000, 1, generator=gen)
print(mode_share(healthy, [-2.0, 2.0]))
print(mode_share(collapsed, [-2.0, 2.0]))
```

```text
[0.5, 0.5]
[0.0, 1.0]
```

- `samples` is `(N, 1)`, the centres `(2,)`: the subtraction broadcasts into
  an `(N, 2)` table of distances; `argmin(dim=1)` picks each example's
  nearest centre.
- The healthy set is split half and half over the two clusters; the
  collapsed set is entirely in one. Every example of both sets is
  "realistic": looking at them one by one shows no difference, only counting
  does.

Images have no cluster centres; the same idea is applied by running the
generated images through a pretrained classifier and looking at the class
distribution.

## Remedies

- **A smaller learning rate and time for the discriminator:** collapse often
  comes from the game oscillating fast.
- **Label smoothing** (previous note): when the discriminator is not
  overconfident a smoother derivative reaches the generator.
- **Changing the loss:** alternatives such as the Wasserstein loss were
  proposed to calm training; they are used together with extra terms such as
  a gradient penalty.
- **Another model family:** the diffusion models from the Generative AI
  Fundamentals module have largely replaced GANs in image generation
  because of their stable training and variety. GANs are still used where
  fast single-step generation is needed.
