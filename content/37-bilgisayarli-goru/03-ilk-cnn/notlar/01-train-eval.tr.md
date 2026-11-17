`model.train()` ve `model.eval()` ağın **kipini** değiştirir. Ağırlıklara
dokunmazlar; yalnızca eğitimde ve tahminde farklı davranan katmanları
etkilerler: `Dropout` (rastgele nöron kapatma) ve `BatchNorm` (yığın
istatistikleriyle normalleştirme).

```python
import torch
from torch import nn

torch.manual_seed(0)
net = nn.Sequential(nn.Linear(4, 64), nn.Dropout(0.5))
x = torch.ones(1, 4)
net.train()
print(torch.equal(net(x), net(x)))
net.eval()
print(torch.equal(net(x), net(x)))
print(net.training)
with torch.no_grad():
    y = net(x)
print(y.requires_grad, net(x).requires_grad)
```

```text
False
True
False
False True
```

- Eğitim kipinde `Dropout` her çağrıda başka nöronları kapattığı için aynı
  girdi iki farklı çıktı veriyor.
- Değerlendirme kipinde `Dropout` kapalı: çıktı her seferinde aynı.
- `torch.no_grad()` ayrı bir şey: kipi değiştirmiyor, türev kaydını
  kapatıyor. İçinde hesaplanan sonucun `requires_grad`'ı `False`; bellek ve
  zaman kazandırıyor.

| | `model.eval()` | `torch.no_grad()` |
|---|---|---|
| Ne değişir | Dropout ve BatchNorm davranışı | Türev kaydı |
| Ne zaman | Doğrulama, test, tahmin | Doğrulama, test, tahmin |
| Unutulursa | Sonuçlar oynak ya da yanlış | Gereksiz bellek |

Ölçerken ikisi birlikte kullanılır. Ölçtükten sonra eğitime dönerken
`model.train()` unutulmamalı; dersteki `train_epoch` bu yüzden onunla başlıyor.
