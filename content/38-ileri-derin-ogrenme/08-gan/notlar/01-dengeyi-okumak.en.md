In an ordinary network you are glad when the loss falls. A GAN is different:
the two networks' losses pull against each other, and in a training run that
goes well neither of them goes to zero; they oscillate around a **balance**
value. Knowing that value lets you read the loss curve.

## The losses at balance

At balance the discriminator says 0.5 to every example. As a logit that is 0
(`sigmoid(0) = 0.5`). Then we can compute both losses exactly:

```python
import math
import torch
from torch import nn

loss_fn = nn.BCEWithLogitsLoss()
half = torch.zeros(64, 1)
ones, zeros = torch.ones(64, 1), torch.zeros(64, 1)
d_loss = loss_fn(half, ones) + loss_fn(half, zeros)
g_loss = loss_fn(half, ones)
print(round(d_loss.item(), 3), round(g_loss.item(), 3))
print(round(2 * math.log(2), 3), round(math.log(2), 3))
```

```text
1.386 0.693
1.386 0.693
```

- The discriminator's loss is the sum of two terms, at balance
  `2 · ln 2 ≈ 1.386`; the generator's is `ln 2 ≈ 0.693`.
- If the losses wander around these values during training, the game is
  still going on.

## Bad signs

- **The discriminator's loss drops to zero:** the discriminator has won. It
  says "0" to the fakes very confidently; the generator's loss grows, but its
  derivative points in no useful direction. Usually this means the
  discriminator learns much faster than the generator (lower the learning
  rate, shrink the discriminator).
- **The generator's loss drops to zero:** the generator may be fooling the
  discriminator with a single trick; do not take it as good without looking
  at the examples. The next note covers the best-known form of this.

## Label smoothing

A simple way to keep the discriminator from becoming overconfident is to
give the real examples a target of 0.9 instead of 1 (label smoothing). Let us
compare a very confident discriminator (logit 6, probability ≈ 0.998) under
both targets:

```python
sure = torch.full((64, 1), 6.0)
print(round(loss_fn(sure, ones).item(), 3))
print(round(loss_fn(sure, torch.full((64, 1), 0.9)).item(), 3))
```

```text
0.002
0.602
```

With target 1 overconfidence is hardly punished at all; with target 0.9 the
loss grows noticeably and the discriminator is pushed not to be so sure of
itself. Only the real examples' target is smoothed; the fakes' stays 0.
