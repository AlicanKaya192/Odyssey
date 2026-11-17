The most common mistake when writing a CNN is getting the input count of the
`Linear` after `Flatten` wrong. Learning to read the error message saves
time:

```python
import torch
from torch import nn

wrong = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1),
    nn.MaxPool2d(4),
    nn.Flatten(),
    nn.Linear(128, 3),
)
try:
    wrong(torch.zeros(2, 1, 16, 16))
except RuntimeError as error:
    print(error)

lazy = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1),
    nn.MaxPool2d(4),
    nn.Flatten(),
    nn.LazyLinear(3),
)
print(tuple(lazy(torch.zeros(2, 1, 16, 16)).shape))
print(tuple(lazy[3].weight.shape))
```

```text
addmm: mat1 and mat2 shapes cannot be multiplied (2x256 and 128x3)
(2, 3)
(3, 256)
```

- `mat1` is the flattened data: 2 pictures, 256 numbers each (`16 × 4 × 4`).
- `mat2` is the `Linear`'s weight (turned for the product): it expects 128
  inputs. The two numbers (256 and 128) should have been equal.
- The fix: write the second number of the first matrix in the message (256)
  into the `Linear`. Or `nn.LazyLinear`: it finds its input count on the first
  run (its weight is created only then).

Running the network once with a fake input (`torch.zeros`) right after
building it catches this error before training starts.
