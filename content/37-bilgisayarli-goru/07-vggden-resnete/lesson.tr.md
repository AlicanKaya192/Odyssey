# VGG'den ResNet'e

Kendi küçük CNN'lerimizi kurduk. Gerçek dünyada sık kullanılan mimariler
aynı parçalardan yapılmış, ama iki fikirle çok daha derine gidiyor. Bu
bölümde ikisini göreceğiz: **VGG**'nin "hep küçük çekirdek" kuralı ve
**ResNet**'in **artık bağlantısı** (residual connection). Sonra
torchvision'daki gerçek `resnet18` mimarisini açıp içine bakacağız. Hazır
eğitilmiş ağırlık indirmeyeceğiz (`weights=None`): mimari ve parametre
sayısı için ağırlıklara gerek yok.

## VGG: üst üste küçük çekirdekler

VGG ailesinin fikri sade: yalnızca 3 × 3 evrişim kullan, birkaç tanesini üst
üste koy, sonra havuzla. İki 3 × 3 evrişim art arda gelince alıcı alan 5 × 5
oluyor: tek bir 5 × 5 çekirdeğin gördüğü kadar. Ama daha az parametreyle ve
arada bir ReLU daha:

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

İki küçük çekirdek, büyüğünün parametresinin yaklaşık %72'siyle aynı alanı
görüyor ve araya bir doğrusal olmayan adım katıyor. Bir VGG **bloğu** bu
yüzden "birkaç 3 × 3 evrişim + havuzlama"dır:

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

## Derinliğin sorunu

Daha derin ağ daha karmaşık desen öğrenebilir; o hâlde katman eklemek yeter
mi? Normalleştirmesiz, düz bir ağı (evrişim + ReLU, üst üste) farklı
derinliklerde kurup bir kaybın **ilk katmana** ulaşan türevine bakalım.
Türevin büyüklüğünü 10'un kuvveti olarak yazıyoruz: `-4`, 10⁻⁴ civarı demek.

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

Katman arttıkça ilk katmanın türevi akıl almaz biçimde küçülüyor: her
katman geri gelen sinyali biraz daha söndürüyor. Türev neredeyse sıfırsa
ilk katmanlar **öğrenemez**. Buna **kaybolan gradyan** (vanishing gradient)
denir. Uygulamada daha derin düz ağların daha **kötü** sonuç verdiği bile
gözlendi; sorun aşırı öğrenme değil, eğitilememek.

## ResNet: artık bağlantı

ResNet'in çözümü bir toplama işareti. Bir blok girdiyi dönüştürüp yerine
koymak yerine **girdinin üstüne ekler**: `çıktı = x + f(x)`. Blok yalnızca
"ne değişmeli" kısmını (artığı) öğrenir. Geri yayılımda türev bu kestirme
yoldan ilk katmanlara azalmadan ulaşır. ResNet her evrişimden sonra
**BatchNorm** da kullanır: değerleri her katmanda ortalaması 0, sapması 1
civarına çeker (Derin Öğrenmenin Temelleri modülündeki normalleştirme
bölümünü hatırla).

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

Aynı sayıda evrişim katmanı (her blokta iki), ama ilk katmanın türevi
derinlikle sönmüyor. 2015'te bu fikir 150'yi aşkın katmanlı ağları
eğitilebilir yaptı.

- Bloğun girdisi ile çıktısı **aynı şekilde** olmalı ki toplanabilsin.
- `bias=False`: hemen ardından gelen BatchNorm kendi sabitini taşıdığı için
  evrişimin sabiti gereksiz.

## torchvision'daki ResNet-18

torchvision ünlü mimarileri hazır veriyor. `weights=None` ağırlıkları rastgele
başlatıyor; internet gerekmiyor.

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

- 11 milyondan fazla parametre: bizim ağlarımızdan binlerce kat büyük.
- Yapı tanıdık: başta 7 × 7 evrişim ve havuzlama (`conv1`, `maxpool`),
  ortada artık bloklardan oluşan dört aşama (`layer1`…`layer4`), sonda
  küresel ortalama havuzlama (`avgpool`) ve sınıf puanlarını veren `fc`.
- Son katman 1000 sınıf için: ağ ilk kez ImageNet adlı büyük bir veri
  setinde (1000 sınıf, bir milyonu aşkın fotoğraf) eğitilmek üzere tasarlandı.
- 20 evrişimin 17'si 3 × 3 ya da 7 × 7; kalan 3'ü, kanal sayısı değişen
  bloklarda kestirme yolu uyduran 1 × 1 evrişimler (notlarda).

## Kendi problemine uyarlamak

Üç sınıf için son katmanı değiştirmek yeter. `avgpool` küresel olduğu için ağ
her boyda resmi kabul ediyor:

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

Bir sonraki bölümde tam bunu yapacağız: başka bir görevde eğitilmiş bir ağın
son katmanını değiştirip yeni göreve uyarlamak, yani **transfer öğrenme**.

## Özet

- VGG: hep 3 × 3; iki küçük çekirdek bir büyüğünün alanını daha az
  parametreyle görür.
- Düz derin ağda ilk katmanların türevi söner (kaybolan gradyan).
- ResNet bloğu: `çıktı = ReLU(x + f(x))`; türev kestirmeden akar.
- `models.resnet18(weights=None)`: mimari, internetsiz; `fc`'yi değiştirerek
  uyarlanır.
