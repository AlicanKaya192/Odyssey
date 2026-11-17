Bir evrişim katmanının çıktı boyu:

$$\text{çıkış} = \left\lfloor \frac{H + 2P - K}{S} \right\rfloor + 1$$

| Ayar | Etkisi |
|---|---|
| `kernel_size=3, padding=1, stride=1` | Boy aynı kalır |
| `kernel_size=5, padding=2, stride=1` | Boy aynı kalır |
| `stride=2` | Boy yaklaşık yarıya iner |
| `padding=0` | Her kenardan `K // 2` piksel gider |
| `padding="same"` | Boyu korumak için dolguyu PyTorch hesaplar (yalnızca adım 1) |

Formülü katmanın kendisiyle karşılaştıralım:

```python
import torch
from torch import nn


def out_size(h, k, s=1, p=0):
    return (h + 2 * p - k) // s + 1


x = torch.zeros(1, 1, 28, 28)
for k, s, p in [(3, 1, 0), (5, 1, 2), (3, 2, 1), (7, 2, 3)]:
    real = nn.Conv2d(1, 1, k, stride=s, padding=p)(x).shape[-1]
    print(k, s, p, out_size(28, k, s, p), real)
same = nn.Conv2d(1, 1, 5, padding="same")
print(same(x).shape[-1])
```

```text
3 1 0 26 26
5 1 2 28 28
3 2 1 14 14
7 2 3 14 14
28
```

Formül her satırda katmanla aynı sonucu veriyor. Tek sayılı çekirdek (3, 5,
7) kullanmanın sebebi de burada: `K // 2` dolgu iki yana eşit dağılıyor ve
çıktının ortası girdinin ortasına denk geliyor.
