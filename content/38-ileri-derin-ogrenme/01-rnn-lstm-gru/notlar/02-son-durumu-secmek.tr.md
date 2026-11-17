Paketlemeden de dolgulu bir dizinin son gerçek adımını bulabiliriz: `out`
her adımın durumunu tuttuğuna göre her diziden `uzunluk − 1`. konumu seçmek
yeter. Bunun için iki dizinli seçim kullanılır: birinci dizin hangi dizi,
ikincisi hangi adım.

```python
import torch
from torch import nn

torch.manual_seed(0)
lstm = nn.LSTM(4, 3, batch_first=True, bidirectional=True)
x = torch.randn(3, 6, 4)
lengths = torch.tensor([6, 4, 2])
out, (h, c) = lstm(x)
last = out[torch.arange(3), lengths - 1]
print(tuple(out.shape), tuple(last.shape))
print(torch.allclose(out[:, -1, :3], h[-2]))
print(torch.allclose(out[:, 0, 3:], h[-1]))
summary = torch.cat([h[-2], h[-1]], dim=1)
print(tuple(summary.shape))
```

```text
(3, 6, 6) (3, 6)
True
True
(3, 6)
```

- `out[torch.arange(3), lengths - 1]`: 0. diziden 5., 1. diziden 3., 2.
  diziden 1. adım. Sonuç `(3, 6)`.
- Çift yönlü ağda `out`'un ilk 3 sayısı ileri, son 3 sayısı geri yön.
  İleri yön **son** adımda bitiyor (`h[-2]`), geri yön **ilk** adımda
  (`h[-1]`, sağdan sola okuduğu için). İki `True` bunu gösteriyor.
- Çift yönlü özet için ikisini yan yana koymak yaygın: `(B, 2H)`.

## Dikkat: çift yönlü ağ ve dolgu

Geri yön diziyi sondan başa okur. Dolgulu bir dizide "son" dolgunun sonu
olur: geri yön önce dolguları okur ve özeti bozar. Yukarıdaki `x`'te dolgu
yoktu; gerçek dolgulu veride çift yönlü ağa **her zaman paketli** girdi
ver. İleri yönde ise son gerçek adımı seçmek paketlemeyle aynı sonucu verir.

| Durum | Son durum için |
|---|---|
| Tek yön, dolgulu | Paketle ya da `out[arange(B), lengths - 1]` |
| Çift yön, dolgulu | Paketle (`pack_padded_sequence`) |
| Dolgu yok | `h[-1]` (çift yönde `h[-2]`, `h[-1]`) |
