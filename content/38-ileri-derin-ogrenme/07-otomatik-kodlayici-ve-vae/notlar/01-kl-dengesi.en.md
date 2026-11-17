In a VAE's loss two terms pull against each other: reconstruction wants a good
copy, KL wants the codes to stay close to a standard normal. Let us see with
small tensors when the KL grows:

```python
import torch


def kl_term(mu, logvar):
    return -0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))


zeros = torch.zeros(1, 4)
print(kl_term(torch.ones(1, 4), zeros).item())
print(kl_term(zeros, torch.full((1, 4), -2.0)).item() > 0)
```

```text
2.0
True
```

- When the mean moves away from 0 the KL grows: for `mu = 1` in every
  dimension, `0.5 · 1² = 0.5` each, 2 over four dimensions.
- It also grows when the variance shrinks below 1 (`logvar = −2`): a code
  trying to collapse to a single point is penalised.

## Balancing with β

Writing the loss as `reconstruction + β · KL` is common (β-VAE):

| β | What happens |
|---|---|
| Small (0.1) | Excellent reconstruction; a messy latent space, drawn codes can give meaningless images |
| 1 | The classic VAE |
| Large (4+) | Tidy, independent codes; blurry images |
| Very large | The code stops carrying the input, every input gets the same average image (posterior collapse) |

Raising β slowly from 0 to 1 at the start of training (KL annealing) is one
of the known ways to prevent posterior collapse.
