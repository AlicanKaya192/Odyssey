The `tau` (temperature) in NT-Xent divides the similarities before the
softmax. A cosine similarity stays between -1 and 1; with `tau = 1` the logits
sit in an equally narrow range and the softmax comes out almost flat. As
`tau` shrinks, the same differences in similarity grow and the probability
gathers on the most similar candidates.

```python
import torch
import torch.nn.functional as F


def nt_xent(z1, z2, tau=0.1):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    sim = z @ z.T / tau
    sim.fill_diagonal_(float("-inf"))
    n = len(z1)
    target = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(sim, target)


gen = torch.Generator().manual_seed(0)
z1 = torch.randn(8, 16, generator=gen)
z2 = z1 + 0.5 * torch.randn(8, 16, generator=gen)
for tau in [1.0, 0.5, 0.1]:
    print(tau, round(nt_xent(z1, z2, tau).item(), 2))
```

```text
1.0 1.85
0.5 1.14
0.1 0.01
```

- Here the partners (`z2`, a noisy copy of `z1`) are already clearly more
  similar than the others. With `tau = 1` that difference is squashed by the
  softmax and the loss stays high; as `tau` shrinks the partner's probability
  approaches 1 and the loss falls.
- The loss value itself cannot be compared across `tau`s; `tau` is a setting
  (hyperparameter), best chosen with validation. Values between 0.05 and 0.5
  are common in published work.
- A small `tau` punishes **hard negatives** (the strangers most similar to the
  partner) heavily. If chosen too small, training also tries hard to separate
  two different images that are actually of the same class: two different
  circles are each other's negatives. This is a known limit of contrastive
  learning.
