1 × 1 evrişim ilk bakışta anlamsız görünür: tek pikseli kendisiyle
çarpmak. Ama girdi çok kanallıysa her konumda **kanalları karıştırır**: her
çıkış kanalı, giriş kanallarının ağırlıklı toplamı. Komşu piksellere hiç
bakmaz.

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

- 64 kanaldan 128 kanala, adım 2 ile boyu da yarıya indirerek: 8192
  parametre (64 × 128).
- ResNet'te bir aşamadan ötekine geçerken kanal sayısı ikiye katlanıyor ve
  harita küçülüyor. O blokta `x` ile `f(x)` aynı şekilde olmadığı için
  toplanamaz; kestirme yol bir 1 × 1 evrişim (ve BatchNorm) ile `f(x)`'in
  şekline getiriliyor. torchvision bunu `downsample` diye adlandırıyor.
- Daha büyük ResNet'ler (50 ve sonrası) 1 × 1 evrişimi bir de **darboğaz**
  (bottleneck) için kullanır: önce kanalları azaltıp ucuz bir 3 × 3 evrişim
  yapar, sonra yeniden artırır.
