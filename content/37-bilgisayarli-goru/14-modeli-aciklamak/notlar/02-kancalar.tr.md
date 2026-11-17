Kancalar ağın koduna dokunmadan içine bakmanın yolu, ama sökülmezlerse
sessizce birikir. Defterde aynı hücreyi iki kez çalıştırmak kancayı iki kez
takar.

```python
import torch
from torch import nn

layer = nn.Linear(2, 2)
calls = []
for _ in range(3):
    layer.register_forward_hook(lambda module, inputs, output: calls.append(1))
layer(torch.zeros(1, 2))
print(len(layer._forward_hooks), len(calls))
```

```text
3 3
```

Üç kez takılan kanca, tek ileri geçişte üç kez çağrıldı. Doğrusu tutamacı
saklayıp iş bitince sökmek; `try` / `finally` hata çıksa bile sökülmesini
sağlar:

```python
def output_shapes(model, x):
    shapes = []
    handles = [part.register_forward_hook(
        lambda module, inputs, output: shapes.append(tuple(output.shape)))
        for part in model]
    try:
        model(x)
    finally:
        for handle in handles:
            handle.remove()
    return shapes


net = nn.Sequential(
    nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten()
)
print(output_shapes(net, torch.zeros(1, 1, 8, 8)))
print(output_shapes(net, torch.zeros(1, 1, 8, 8)))
print([len(part._forward_hooks) for part in net])
```

```text
[(1, 4, 8, 8), (1, 4, 8, 8), (1, 4, 4, 4), (1, 64)]
[(1, 4, 8, 8), (1, 4, 8, 8), (1, 4, 4, 4), (1, 64)]
[0, 0, 0, 0]
```

- İki çağrıda da dört katman, dört şekil: kancalar her seferinde söküldü.
- Geri yönde de kanca var: `register_full_backward_hook` bir katmandan geçen
  gradyanı verir. Dersteki gibi `torch.autograd.grad` ile gradyanı doğrudan
  istemek çoğu zaman daha sade.
- `_forward_hooks` alt çizgiyle başlıyor: PyTorch'un iç alanı. Burada yalnızca
  saymak için bakıyoruz; kodda ona yazılmaz.
