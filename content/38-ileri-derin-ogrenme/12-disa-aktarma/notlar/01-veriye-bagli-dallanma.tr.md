Dışa aktarma modeli **bir örnek girdiyle** izler. Modelde girdinin
değerine bağlı bir `if` varsa izleme o örneğin gittiği dalı görür, öbür dalı
hiç görmez. Eski `torch.jit.trace` bunu sessizce kabul eder:

```python
import warnings
import torch
from torch import nn

warnings.simplefilter("ignore")


class Branchy(nn.Module):
    def forward(self, x):
        if x.sum() > 0:
            return x * 2
        return x * -1


model = Branchy()
pos, neg = torch.ones(3), -torch.ones(3)
traced = torch.jit.trace(model, pos)
print(model(neg).tolist(), traced(neg).tolist())
```

```text
[1.0, 1.0, 1.0] [-2.0, -2.0, -2.0]
```

- İzleme pozitif bir girdiyle yapıldı; kaydedilen hesap "iki ile çarp".
  Negatif girdide asıl model `x * -1` diyor (`1.0`), izlenen model hâlâ iki
  ile çarpıyor (`-2.0`). Hata yok, uyarı bastırılınca hiçbir iz yok: yanlış
  sonuç.
- `warnings.simplefilter("ignore")` burada yalnızca çıktıyı temiz tutmak
  için; gerçek kodda `trace`'in uyarılarını bastırma, tam da bunu söylüyorlar.

`torch.export` aynı modeli kabul etmez; dalın veriye bağlı olduğunu görüp
hata verir. Her iki dal da gerekiyorsa `torch.cond` ile yazılır:

```python
try:
    torch.export.export(model, (pos,))
except Exception as e:
    print(type(e).__name__)


class CondNet(nn.Module):
    def forward(self, x):
        return torch.cond(x.sum() > 0, lambda t: t * 2, lambda t: t * -1, (x,))


ep = torch.export.export(CondNet(), (pos,))
print(ep.module()(pos).tolist(), ep.module()(neg).tolist())
```

```text
GuardOnDataDependentSymNode
[2.0, 2.0, 2.0] [1.0, 1.0, 1.0]
```

- Hatanın adı uzun ama anlamı açık: "veriye bağlı bir ifade üzerinde koruma
  kuramıyorum".
- `torch.cond(koşul, doğruysa, yanlışsa, (girdiler,))` iki dalı da grafiğe
  koyar; dışa aktarılan model iki girdide de doğru.

Dışa aktarmadan sonra modeli her zaman **birkaç farklı girdiyle** asıl
modelle karşılaştır. Şekle bağlı dallanma (grup boyu, dizi uzunluğu) için de
aynısı geçerli: dışa aktarırken örnek seçerken hangi şekillerin
kullanılacağını düşün.
