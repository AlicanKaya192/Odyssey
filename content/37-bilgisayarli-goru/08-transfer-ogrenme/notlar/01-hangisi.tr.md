Hangi yolu seçeceğin iki soruya bağlı: hedefte ne kadar veri var, hedef
kaynağa ne kadar benziyor?

| | Hedef kaynağa benziyor | Hedef kaynaktan farklı |
|---|---|---|
| **Az veri** | Özellik çıkarma (gövde donuk) | İnce ayar, düşük öğrenme oranı, dikkatli |
| **Çok veri** | İnce ayar | İnce ayar ya da sıfırdan |

İnce ayarda sık kullanılan bir yöntem, gövdeye ve başa **farklı öğrenme
oranı** vermek: baş yeni ve rastgele, hızlı öğrenmeli; gövde zaten iyi,
yavaşça kaymalı. Optimizer'a parametre **grupları** verilir:

```python
import torch
from torch import nn

features = nn.Sequential(nn.Conv2d(1, 8, 3), nn.ReLU(),
                         nn.AdaptiveAvgPool2d(1), nn.Flatten())
head = nn.Linear(8, 2)
optimizer = torch.optim.Adam([
    {"params": features.parameters(), "lr": 1e-4},
    {"params": head.parameters(), "lr": 1e-2},
])
for group in optimizer.param_groups:
    print(group["lr"], sum(p.numel() for p in group["params"]))
```

```text
0.0001 80
0.01 18
```

Başka bir alışkanlık: önce yalnızca başı birkaç tur eğitmek (gövde donuk),
sonra gövdeyi çözüp küçük öğrenme oranıyla birlikte eğitmek. Rastgele başın
ilk büyük hataları, iyi gövdeyi bozmadan önce düzelmiş olur.
