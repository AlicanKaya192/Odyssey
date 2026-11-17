The output size of a convolution layer:

$$\text{output} = \left\lfloor \frac{H + 2P - K}{S} \right\rfloor + 1$$

| Setting | Effect |
|---|---|
| `kernel_size=3, padding=1, stride=1` | The size stays the same |
| `kernel_size=5, padding=2, stride=1` | The size stays the same |
| `stride=2` | The size roughly halves |
| `padding=0` | `K // 2` pixels go from each edge |
| `padding="same"` | PyTorch computes the padding that keeps the size (stride 1 only) |

Let us compare the formula with the layer itself:

```python
import torch
from torch import nn


def out_size(h, k, s=1, p=0):
    return (h + 2 * p - k) // s + 1


x = torch.zeros(1, 1, 28, 28)
for k, s, p in [(3, 1, 0), (5, 1, 2), (3, 2, 1), (7, 2, 3)]:
    real = nn.Conv2d(1, 1, k, stride=s, padding=p)(x).shape[-1]
    print(k, s, p, out_size(28, k, s, p), real)
same = nn.Conv2d(1, 1, 5, padding="same")
print(same(x).shape[-1])
```

```text
3 1 0 26 26
5 1 2 28 28
3 2 1 14 14
7 2 3 14 14
28
```

The formula gives the same result as the layer in every row. This is also why
odd kernels (3, 5, 7) are used: the `K // 2` padding splits evenly between the
two sides and the centre of the output lines up with the centre of the input.
