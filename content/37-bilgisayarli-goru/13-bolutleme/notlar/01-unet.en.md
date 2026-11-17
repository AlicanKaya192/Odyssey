The encoder–decoder in the lesson loses fine detail (the exact border of a
shape) while shrinking; the transposed convolution has to guess it from
scratch. For this, **U-Net** also gives the decoder the encoder's output of
the same size: a **skip connection**. The two outputs are placed side by side
along the channels (`torch.cat(..., dim=1)`).

```python
import torch
from torch import nn


class TinyUNet(nn.Module):
    def __init__(self, classes=4):
        super().__init__()
        self.down = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU())
        self.middle = nn.Sequential(
            nn.MaxPool2d(2), nn.Conv2d(16, 32, 3, padding=1), nn.ReLU()
        )
        self.up = nn.ConvTranspose2d(32, 16, 2, stride=2)
        self.head = nn.Conv2d(32, classes, 1)

    def forward(self, x):
        skip = self.down(x)
        deep = self.middle(skip)
        joined = torch.cat([self.up(deep), skip], dim=1)
        print(skip.shape, deep.shape, joined.shape)
        return self.head(joined)


torch.manual_seed(0)
print(TinyUNet()(torch.zeros(2, 1, 32, 32)).shape)
```

```text
torch.Size([2, 16, 32, 32]) torch.Size([2, 32, 16, 16]) torch.Size([2, 32, 32, 32])
torch.Size([2, 4, 32, 32])
```

- `skip`: full size, 16 channels (fine detail). `deep`: half size, 32
  channels (wide context).
- The enlarged `deep` and `skip` side by side: 16 + 16 = 32 channels. The
  last layer gets the class scores from these 32 channels.
- In a real U-Net this shrinking and growing is repeated four or five times;
  drawn out it looks like the letter "U", hence the name.

`torch.cat` needs the sizes to match: if the picture size is not a power of 2
(for example 33), the enlarged output comes out one pixel short and `cat`
raises an error.
