Which path to choose depends on two questions: how much data does the target
have, and how similar is the target to the source?

| | Target similar to the source | Target different from the source |
|---|---|---|
| **Little data** | Feature extraction (frozen body) | Fine-tuning, low learning rate, carefully |
| **Plenty of data** | Fine-tuning | Fine-tuning or from scratch |

A common method in fine-tuning gives the body and the head **different
learning rates**: the head is new and random and should learn fast; the body
is already good and should shift slowly. The optimizer is given parameter
**groups**:

```python
import torch
from torch import nn

features = nn.Sequential(nn.Conv2d(1, 8, 3), nn.ReLU(),
                         nn.AdaptiveAvgPool2d(1), nn.Flatten())
head = nn.Linear(8, 2)
optimizer = torch.optim.Adam([
    {"params": features.parameters(), "lr": 1e-4},
    {"params": head.parameters(), "lr": 1e-2},
])
for group in optimizer.param_groups:
    print(group["lr"], sum(p.numel() for p in group["params"]))
```

```text
0.0001 80
0.01 18
```

Another habit: first train only the head for a few epochs (body frozen), then
unfreeze the body and train both with a small learning rate. The random
head's first big mistakes are fixed before they can damage the good body.
