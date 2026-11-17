Haritayı küçültmenin iki yolu var: havuzlama ya da **adımı 2 olan
evrişim**. İkisi aynı şekli veriyor ama farklı çalışıyor:

```python
import torch
from torch import nn

x = torch.zeros(1, 8, 16, 16)
pool = nn.MaxPool2d(2)
strided = nn.Conv2d(8, 8, kernel_size=3, stride=2, padding=1)
print(tuple(pool(x).shape), tuple(strided(x).shape))
print(sum(p.numel() for p in pool.parameters()))
print(sum(p.numel() for p in strided.parameters()))
```

```text
(1, 8, 8, 8) (1, 8, 8, 8)
0
584
```

| | Maksimum havuzlama | Adımlı evrişim |
|---|---|---|
| Parametre | Yok | Var (öğrenilir) |
| Ne bırakır | Karenin en büyüğünü | Öğrenilmiş bir karışımı |
| Nerede görülür | Klasik CNN'ler (VGG gibi) | Modern ağlar, ResNet'in bölümleri |

Adımlı evrişim küçültmeyi de öğreniyor; bedeli fazladan parametre ve hesap.
Bu modüldeki küçük ağlarda havuzlama yeterli ve daha sade.
