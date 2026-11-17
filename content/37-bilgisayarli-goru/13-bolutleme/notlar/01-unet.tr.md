Dersteki kodlayıcı–çözücü küçültürken ince ayrıntıyı (şeklin tam sınırını)
kaybediyor; ters evrişim onu sıfırdan tahmin etmek zorunda. **U-Net** bunun
için çözücüye, kodlayıcının aynı boydaki çıktısını da veriyor: **atlama
bağlantısı** (skip connection). İki çıktı kanal boyunca yan yana konuyor
(`torch.cat(..., dim=1)`).

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

- `skip`: tam boy, 16 kanal (ince ayrıntı). `deep`: yarım boy, 32 kanal
  (geniş bağlam).
- Büyütülen `deep` ile `skip` yan yana: 16 + 16 = 32 kanal. Son katman bu
  32 kanaldan sınıf puanlarını çıkarıyor.
- Gerçek U-Net'te bu küçültme ve büyütme dört beş kez tekrarlanır; çizildiğinde
  "U" harfine benzediği için adı böyle.

`torch.cat` boyların aynı olmasını ister: resim boyu 2'nin kuvveti değilse
(örneğin 33) büyütülen çıktı bir piksel kısa kalır ve `cat` hata verir.
