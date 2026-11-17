ResNet uses `BatchNorm2d` after every convolution. Let us look briefly at
what it does and why it behaves differently in training and in prediction:

```python
import torch
from torch import nn

torch.manual_seed(0)
bn = nn.BatchNorm2d(4)
x = torch.randn(8, 4, 5, 5) * 3 + 10
y = bn(x)
print(abs(y.mean().item()) < 1e-5, round(y.std().item(), 2))
print(sum(p.numel() for p in bn.parameters()))
print([name for name, _ in bn.named_buffers()])
bn.eval()
print(abs(bn(x).mean().item()) > 1)
```

```text
True 1.0
8
['running_mean', 'running_var', 'num_batches_tracked']
True
```

- **In training mode** it normalises each channel with **that batch's** mean
  and standard deviation: an input with a mean of 10 became an output with a
  mean of 0.
- It has two learned parameters (a scale and a shift per channel): 8 for 4
  channels. So the network can undo the normalisation if it wants to.
- It also keeps **buffers**: `running_mean`, `running_var`. These are not
  learned; they are a moving average of the batch statistics during training.
- **In evaluation mode** these moving averages are used instead of the batch.
  After a single step the moving average has not yet reached the real mean
  (10), so the output's mean is far from zero.

The upshot: if `model.eval()` is forgotten when predicting with a BatchNorm
network, each batch's own statistics are used; even a single-picture
prediction can come out wrong. This difference comes back in transfer
learning.
