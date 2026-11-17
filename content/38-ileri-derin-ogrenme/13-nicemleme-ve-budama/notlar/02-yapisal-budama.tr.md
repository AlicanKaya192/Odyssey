Seyrek budama sıfırları matrisin içinde bırakır. **Yapısal budama** bütün
bir satırı, yani bir nöronu sıfırlar; o nöron artık hiçbir girdiye bağlı
değildir ve katmandan gerçekten çıkarılabilir. Model küçülür ve sıradan
donanımda da hızlanır.

```python
import torch
import torch.nn.utils.prune as prune
from torch import nn

torch.manual_seed(0)
fc1, fc2 = nn.Linear(6, 64), nn.Linear(64, 3)
model = nn.Sequential(fc1, nn.ReLU(), fc2).eval()
prune.ln_structured(fc1, "weight", amount=0.5, n=2, dim=0)
prune.remove(fc1, "weight")
keep = fc1.weight.abs().sum(dim=1) > 0
print(int(keep.sum()), tuple(fc1.weight.shape))
```

```text
32 (64, 6)
```

- `ln_structured(..., n=2, dim=0)`: satırların (dim 0) L2 normuna bakar,
  en küçük yarısını sıfırlar. 64 nörondan 32'si kaldı.
- `prune.remove` budamayı kalıcı yapar (budama maskesini ağırlığa işler).
  Şekil hâlâ `(64, 6)`: yer kazanmak için katmanı yeniden kurmak gerekiyor.

Budanan nöronun ağırlıkları sıfır ama **sapması** sıfır değil: o nöron her
girdiye aynı sabit değeri (`ReLU(sapma)`) veriyor. Onu çıkarırken bu sabiti
bir sonraki katmanın sapmasına katarsak çıktı birebir korunur:

```python
n = int(keep.sum())
small1, small2 = nn.Linear(6, n), nn.Linear(n, 3)
with torch.no_grad():
    small1.weight.copy_(fc1.weight[keep])
    small1.bias.copy_(fc1.bias[keep])
    small2.weight.copy_(fc2.weight[:, keep])
    small2.bias.copy_(fc2.bias + fc2.weight[:, ~keep] @ torch.relu(fc1.bias[~keep]))
small = nn.Sequential(small1, nn.ReLU(), small2).eval()


def count(m):
    return sum(p.numel() for p in m.parameters())


x = torch.randn(10, 6)
with torch.no_grad():
    print(torch.allclose(small(x), model(x), atol=1e-6))
print(count(model), count(small))
```

```text
True
643 323
```

- Küçük model budanmış modelle aynı çıktıyı veriyor; parametre sayısı
  yarısına yakın indi.
- `fc2.weight[:, ~keep] @ relu(fc1.bias[~keep])`: çıkarılan nöronların sabit
  katkısı; sonraki katmanın sapmasına eklendi.

Gerçek ağlarda bu iş evrişim kanallarında yapılır (filtre budama) ve
genellikle her budama adımından sonra kısa bir ince ayar eklenir. Sıra hep
aynı: buda, doğruluğu ölç, gerekirse yeniden eğit, katmanı gerçekten küçült.
