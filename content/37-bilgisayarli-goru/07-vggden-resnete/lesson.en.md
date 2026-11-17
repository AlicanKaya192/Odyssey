# From VGG to ResNet

We have built our own small CNNs. The architectures widely used in the real
world are made of the same parts but go much deeper thanks to two ideas. In
this section we look at both: **VGG**'s "always small kernels" rule and
**ResNet**'s **residual connection**. Then we open torchvision's real
`resnet18` architecture and look inside. We will not download pretrained
weights (`weights=None`): the architecture and the parameter count do not
need them.

## VGG: small kernels stacked up

The idea of the VGG family is plain: use only 3 × 3 convolutions, stack a few
of them, then pool. Two 3 × 3 convolutions in a row give a 5 × 5 receptive
field: as much as a single 5 × 5 kernel sees. But with fewer parameters and
one more ReLU in between:

```python
from torch import nn


def count(module):
    return sum(p.numel() for p in module.parameters())


two_small = nn.Sequential(nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(),
                          nn.Conv2d(64, 64, 3, padding=1))
one_big = nn.Conv2d(64, 64, 5, padding=2)
print(count(two_small), count(one_big))
```

```text
73856 102464
```

Two small kernels see the same area with about 72% of the big one's
parameters and add a non-linear step in between. That is why a VGG **block**
is "a few 3 × 3 convolutions + pooling":

```python
import torch


def vgg_block(in_ch, out_ch, convs):
    layers = []
    for i in range(convs):
        layers += [nn.Conv2d(in_ch if i == 0 else out_ch, out_ch, 3, padding=1), nn.ReLU()]
    layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)


small_vgg = nn.Sequential(vgg_block(1, 16, 2), vgg_block(16, 32, 2), vgg_block(32, 64, 2),
                          nn.Flatten(), nn.Linear(64 * 2 * 2, 3))
x = torch.zeros(1, 1, 16, 16)
for block in small_vgg:
    x = block(x)
    print(type(block).__name__, tuple(x.shape))
print(count(small_vgg))
```

```text
Sequential (1, 16, 8, 8)
Sequential (1, 32, 4, 4)
Sequential (1, 64, 2, 2)
Flatten (1, 256)
Linear (1, 3)
72563
```

## The trouble with depth

A deeper network can learn more complex patterns; so is adding layers enough?
Let us build a plain network without normalisation (convolution + ReLU,
stacked) at different depths and look at the gradient of a loss that reaches
the **first layer**. We write the gradient's size as a power of 10: `-4` means
around 10⁻⁴.

```python
import math

import torch.nn.functional as F


class PlainNet(nn.Module):
    def __init__(self, depth):
        super().__init__()
        self.stem = nn.Conv2d(1, 8, 3, padding=1)
        self.layers = nn.ModuleList([nn.Conv2d(8, 8, 3, padding=1) for _ in range(depth)])
        self.head = nn.Linear(8, 3)

    def forward(self, x):
        x = F.relu(self.stem(x))
        for layer in self.layers:
            x = F.relu(layer(x))
        return self.head(x.mean(dim=(2, 3)))


def first_layer_power(model):
    torch.manual_seed(1)
    x = torch.rand(16, 1, 16, 16)
    y = torch.randint(0, 3, (16,))
    F.cross_entropy(model(x), y).backward()
    return math.floor(math.log10(model.stem.weight.grad.norm().item()))


for depth in (4, 20, 40):
    torch.manual_seed(0)
    print(depth, first_layer_power(PlainNet(depth)))
```

```text
4 -4
20 -13
40 -21
```

As layers are added, the first layer's gradient shrinks unimaginably: each
layer dampens the returning signal a little more. If the gradient is almost
zero, the first layers **cannot learn**. This is called the **vanishing
gradient**. In practice deeper plain networks were even seen to give
**worse** results; the problem is not overfitting but failing to train.

## ResNet: the residual connection

ResNet's fix is a plus sign. Instead of transforming the input and putting
the result in its place, a block **adds to the input**: `output = x + f(x)`.
The block learns only the "what should change" part (the residual). In
backpropagation the gradient reaches the first layers through this shortcut
without fading. ResNet also uses **BatchNorm** after every convolution: it
pulls the values in each layer to a mean around 0 and a standard deviation
around 1 (recall the normalisation section of the Deep Learning Fundamentals
module).

```python
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return F.relu(out + x)


class ResNetLike(nn.Module):
    def __init__(self, depth):
        super().__init__()
        self.stem = nn.Conv2d(1, 8, 3, padding=1)
        self.blocks = nn.Sequential(*[ResidualBlock(8) for _ in range(depth // 2)])
        self.head = nn.Linear(8, 3)

    def forward(self, x):
        x = self.blocks(F.relu(self.stem(x)))
        return self.head(x.mean(dim=(2, 3)))


for depth in (4, 20, 40):
    torch.manual_seed(0)
    print(depth, first_layer_power(ResNetLike(depth)))
```

```text
4 -2
20 -1
40 0
```

The same number of convolution layers (two per block), but the first layer's
gradient does not fade with depth. In 2015 this idea made networks with more
than 150 layers trainable.

- The block's input and output must have **the same shape** to be added.
- `bias=False`: the BatchNorm right after carries its own shift, so the
  convolution's bias is unnecessary.

## ResNet-18 in torchvision

torchvision provides famous architectures ready-made. `weights=None` starts
the weights at random; no internet is needed.

```python
from torchvision import models

resnet = models.resnet18(weights=None)
print(count(resnet))
print(" ".join(name for name, _ in resnet.named_children()))
print(resnet.fc)
convs = [m for m in resnet.modules() if isinstance(m, nn.Conv2d)]
print(len(convs), convs[0])
```

```text
11689512
conv1 bn1 relu maxpool layer1 layer2 layer3 layer4 avgpool fc
Linear(in_features=512, out_features=1000, bias=True)
20 Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
```

- More than 11 million parameters: thousands of times bigger than our
  networks.
- The structure is familiar: a 7 × 7 convolution and pooling at the start
  (`conv1`, `maxpool`), four stages of residual blocks in the middle
  (`layer1`…`layer4`), global average pooling (`avgpool`) and `fc`, which gives
  the class scores, at the end.
- The last layer is for 1000 classes: the network was designed to be trained
  first on a large dataset called ImageNet (1000 classes, over a million
  photos).
- 17 of the 20 convolutions are 3 × 3 or 7 × 7; the other 3 are 1 × 1
  convolutions that fit the shortcut in blocks where the channel count changes
  (see the notes).

## Adapting it to your problem

For three classes, replacing the last layer is enough. Since `avgpool` is
global, the network accepts pictures of any size:

```python
resnet.fc = nn.Linear(resnet.fc.in_features, 3)
out = resnet(torch.zeros(2, 3, 64, 64))
print(out.shape, count(resnet))
small = resnet(torch.zeros(2, 3, 32, 32))
print(small.shape)
```

```text
torch.Size([2, 3]) 11178051
torch.Size([2, 3])
```

In the next section we do exactly this: adapting a network trained on another
task to a new task by replacing its last layer, that is, **transfer
learning**.

## Summary

- VGG: always 3 × 3; two small kernels see the area of a big one with fewer
  parameters.
- In a plain deep network the first layers' gradients fade (vanishing
  gradient).
- A ResNet block: `output = ReLU(x + f(x))`; the gradient flows through the
  shortcut.
- `models.resnet18(weights=None)`: the architecture, offline; adapted by
  replacing `fc`.
