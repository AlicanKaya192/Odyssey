There are two ways to shrink a map: pooling or a **convolution with a stride
of 2**. Both give the same shape but work differently:

```python
import torch
from torch import nn

x = torch.zeros(1, 8, 16, 16)
pool = nn.MaxPool2d(2)
strided = nn.Conv2d(8, 8, kernel_size=3, stride=2, padding=1)
print(tuple(pool(x).shape), tuple(strided(x).shape))
print(sum(p.numel() for p in pool.parameters()))
print(sum(p.numel() for p in strided.parameters()))
```

```text
(1, 8, 8, 8) (1, 8, 8, 8)
0
584
```

| | Max pooling | Strided convolution |
|---|---|---|
| Parameters | None | Yes (learned) |
| What it keeps | The square's largest value | A learned mixture |
| Where it appears | Classic CNNs (such as VGG) | Modern networks, parts of ResNet |

A strided convolution also learns how to shrink; the price is extra
parameters and computation. For the small networks in this module, pooling is
enough and simpler.
