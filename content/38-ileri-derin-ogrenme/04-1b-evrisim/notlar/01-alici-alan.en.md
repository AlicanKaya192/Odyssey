How many input steps an output position "sees" is called its **receptive
field**. A single kernel of 5 sees 5 steps. With two convolutions of 5
stacked, each position of the second sees 5 positions of the first, and those
see 9 input steps in total. Instead of computing it we can measure it with
autograd: the derivative of a single output is non-zero only at the input
steps it sees.

```python
import torch
from torch import nn


def receptive_field(model, length=64):
    x = torch.randn(1, 1, length, requires_grad=True)
    out = model(x)
    out[0, 0, out.shape[-1] // 2].backward()
    return int((x.grad[0, 0] != 0).sum())


torch.manual_seed(0)
one = nn.Conv1d(1, 1, 5, padding=2)
two = nn.Sequential(nn.Conv1d(1, 1, 5, padding=2), nn.Conv1d(1, 1, 5, padding=2))
dilated = nn.Sequential(nn.Conv1d(1, 1, 5, padding=2),
                        nn.Conv1d(1, 1, 5, padding=4, dilation=2))
print(receptive_field(one), receptive_field(two), receptive_field(dilated))
```

```text
5 9 13
```

- One layer sees 5 steps, two layers 9: each new layer of size `k` adds
  `k − 1` to the field.
- A **dilated convolution** (`dilation=2`) puts gaps between the kernel's
  elements: the same 5 weights spread over 9 steps. With the same parameters
  two layers see 13 steps.
- To catch the fault, a receptive field as long as the fault pattern is
  enough (8 steps in the lesson). For long dependencies the dilation is
  doubled layer by layer (1, 2, 4, 8, ...): the field grows exponentially
  with the number of layers.

That the network sees the whole window after `AdaptiveMaxPool1d(1)` is not
about the receptive field: every position still looks at a local window; the
pooling only picks the largest of those local answers.
