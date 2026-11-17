`model.train()` and `model.eval()` change the network's **mode**. They do not
touch the weights; they only affect layers that behave differently in
training and in prediction: `Dropout` (switching random neurons off) and
`BatchNorm` (normalising with batch statistics).

```python
import torch
from torch import nn

torch.manual_seed(0)
net = nn.Sequential(nn.Linear(4, 64), nn.Dropout(0.5))
x = torch.ones(1, 4)
net.train()
print(torch.equal(net(x), net(x)))
net.eval()
print(torch.equal(net(x), net(x)))
print(net.training)
with torch.no_grad():
    y = net(x)
print(y.requires_grad, net(x).requires_grad)
```

```text
False
True
False
False True
```

- In training mode `Dropout` switches off different neurons on each call, so
  the same input gives two different outputs.
- In evaluation mode `Dropout` is off: the output is the same every time.
- `torch.no_grad()` is a different thing: it does not change the mode, it
  turns off gradient recording. A result computed inside it has
  `requires_grad` set to `False`; it saves memory and time.

| | `model.eval()` | `torch.no_grad()` |
|---|---|---|
| What changes | Dropout and BatchNorm behaviour | Gradient recording |
| When | Validation, test, prediction | Validation, test, prediction |
| If forgotten | Unstable or wrong results | Wasted memory |

When measuring, both are used together. When going back to training after
measuring, `model.train()` must not be forgotten; that is why the lesson's
`train_epoch` starts with it.
