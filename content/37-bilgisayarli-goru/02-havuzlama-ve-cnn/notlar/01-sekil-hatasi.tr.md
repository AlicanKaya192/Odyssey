CNN yazarken en sık görülen hata, `Flatten`'dan sonraki `Linear`'ın giriş
sayısını yanlış yazmak. Hata mesajını okumayı öğrenmek işi kısaltıyor:

```python
import torch
from torch import nn

wrong = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1),
    nn.MaxPool2d(4),
    nn.Flatten(),
    nn.Linear(128, 3),
)
try:
    wrong(torch.zeros(2, 1, 16, 16))
except RuntimeError as error:
    print(error)

lazy = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1),
    nn.MaxPool2d(4),
    nn.Flatten(),
    nn.LazyLinear(3),
)
print(tuple(lazy(torch.zeros(2, 1, 16, 16)).shape))
print(tuple(lazy[3].weight.shape))
```

```text
addmm: mat1 and mat2 shapes cannot be multiplied (2x256 and 128x3)
(2, 3)
(3, 256)
```

- `mat1` düzleştirilmiş veri: 2 resim, her biri 256 sayı (`16 × 4 × 4`).
- `mat2` `Linear`'ın ağırlığı (çarpım için çevrilmiş hâli): 128 giriş
  bekliyor. İki sayının (256 ve 128) eşit olması gerekiyordu.
- Çözüm: hata mesajındaki ilk matrisin ikinci sayısını (256) `Linear`'a
  yazmak. Ya da `nn.LazyLinear`: giriş sayısını ilk çalıştırmada kendisi
  buluyor (ağırlığı ancak o zaman oluşuyor).

Ağı kurar kurmaz sahte bir girdiyle (`torch.zeros`) bir kez çalıştırmak bu
hatayı eğitim başlamadan yakalar.
