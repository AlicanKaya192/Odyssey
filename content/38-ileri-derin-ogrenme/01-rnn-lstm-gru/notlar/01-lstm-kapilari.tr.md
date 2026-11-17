Gömmeler ve Dil Modelleri modülünde LSTM'in hücresini `c = f · c + i · g`
diye yazmıştık: unutma kapısı `f` eskinin ne kadarının kalacağını, giriş
kapısı `i` yeni bilginin (`g`) ne kadarının yazılacağını söyler; çıkış
kapısı `o` hücreden gizli duruma ne geçeceğini seçer. PyTorch dört parçayı
tek matris çarpımıyla hesaplayıp sonra dörde böler. Tek adımlık hesap için
`nn.LSTMCell` var; formülü elle yazıp onunla karşılaştıralım.

```python
import torch
from torch import nn

torch.manual_seed(0)
cell = nn.LSTMCell(4, 3)
x = torch.randn(2, 4)
h, c = torch.zeros(2, 3), torch.zeros(2, 3)
z = x @ cell.weight_ih.T + cell.bias_ih + h @ cell.weight_hh.T + cell.bias_hh
i, f, g, o = z.chunk(4, dim=1)
c_new = torch.sigmoid(f) * c + torch.sigmoid(i) * torch.tanh(g)
h_new = torch.sigmoid(o) * torch.tanh(c_new)
h_ref, c_ref = cell(x, (h, c))
print(z.shape)
print(torch.allclose(h_new, h_ref), torch.allclose(c_new, c_ref))
```

```text
torch.Size([2, 12])
True True
```

- `z` `(2, 12)`: dört kapının ön değerleri yan yana. PyTorch'un sırası
  **giriş, unutma, aday, çıkış** (`i, f, g, o`). Ağırlıkların bir kısmına
  elle dokunacaksan (aşağıdaki ipucu gibi) bu sırayı bilmek gerekir.
- Kapılar sigmoid'den geçer (0–1 arası "ne kadar"), aday `g` tanh'tan
  (−1–1 arası "ne").
- İki `True`: dört satırlık elle hesap katmanın kendisiyle aynı.

## Ne zaman `LSTMCell`?

| Katman | Ne yapar | Ne zaman |
|---|---|---|
| `nn.LSTM` | Bütün diziyi tek çağrıda okur, hızlı | Hemen her zaman |
| `nn.LSTMCell` | Tek adım; döngüyü sen yazarsın | Her adımda araya bir şey girecekse: önceki çıktıyı girdi yapmak, adım adım karar vermek |

Bilinen bir başlatma ipucu: unutma kapısının yanlılığını başta 1 gibi
pozitif bir değere çekmek, ağın eğitimin başında belleği silmemesini
sağlar. Yanlılıkta unutma kapısının dilimi `[H:2H]`.
