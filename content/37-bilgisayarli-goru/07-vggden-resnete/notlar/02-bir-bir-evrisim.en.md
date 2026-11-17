A 1 × 1 convolution looks pointless at first: multiplying a single pixel by
itself. But if the input has many channels, it **mixes the channels** at each
position: each output channel is a weighted sum of the input channels. It
never looks at neighbouring pixels.

```python
import torch
from torch import nn
from torchvision import models

mix = nn.Conv2d(64, 128, kernel_size=1, stride=2, bias=False)
x = torch.zeros(1, 64, 16, 16)
print(tuple(mix(x).shape), sum(p.numel() for p in mix.parameters()))

resnet = models.resnet18(weights=None)
block = resnet.layer2[0]
print([type(m).__name__ for m in block.downsample])
print(block.downsample[0].kernel_size, block.downsample[0].stride)
```

```text
(1, 128, 8, 8) 8192
['Conv2d', 'BatchNorm2d']
(1, 1) (2, 2)
```

- From 64 channels to 128, also halving the size with stride 2: 8,192
  parameters (64 × 128).
- In ResNet, moving from one stage to the next doubles the channels and
  shrinks the map. In that block `x` and `f(x)` do not have the same shape and
  cannot be added; the shortcut is brought to the shape of `f(x)` with a
  1 × 1 convolution (and BatchNorm). torchvision calls this `downsample`.
- Larger ResNets (50 and up) also use 1 × 1 convolutions for a
  **bottleneck**: first reduce the channels and run a cheap 3 × 3
  convolution, then raise them again.
