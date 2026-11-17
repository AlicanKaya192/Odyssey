PyTorch iki tür maske kabul ediyor: **mantıksal** (`True` = bakma) ve
**sayısal** (bakılmayacak yere `−∞`, gerisine 0; skora eklenir).
`nn.Transformer.generate_square_subsequent_mask` sayısal nedensel maskeyi
hazır verir. İkisi aynı sonucu verir:

```python
import torch
from torch import nn

float_mask = nn.Transformer.generate_square_subsequent_mask(4)
bool_mask = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
print(float_mask[1].tolist())
torch.manual_seed(0)
attn = nn.MultiheadAttention(8, 2, batch_first=True)
x = torch.randn(2, 4, 8)
a, _ = attn(x, x, x, attn_mask=float_mask)
b, _ = attn(x, x, x, attn_mask=bool_mask)
print(torch.allclose(a, b))

everything = torch.tensor([[False, False, False, False], [True, True, True, True]])
out, _ = attn(x, x, x, key_padding_mask=everything)
print(torch.isnan(out[0]).any().item(), torch.isnan(out[1]).any().item())
```

```text
[0.0, 0.0, -inf, -inf]
True
False True
```

- Sayısal maskenin 1. satırı `[0, 0, −∞, −∞]`: 1. konum ilk ikisini görür.
- Son satır bir tuzağı gösteriyor: ikinci dizinin **bütün** anahtarları
  maskelenince softmax'a hep `−∞` girer, sonuç `0 / 0` ve çıkış `nan` olur.
  Uzunluğu 0 olan örnekler veriden çıkarılmalı.

## Sık hatalar

| Hata | Sonuç |
|---|---|
| `key_padding_mask=(ids != 0)` yazmak | Ters maske: model yalnızca dolguya bakar, hata vermez |
| Maskeyi `(B, T)` yerine `(T, B)` vermek | Şekil hatası ya da yanlış dizilere uygulanan maske |
| Dil modelinde nedensel maskeyi unutmak | Eğitim kaybı çok iyi, üretim çok kötü: model cevabı görüyordu |
| Bütün konumları maskelemek | `nan` çıkış, `nan` kayıp |

Üçüncü hata en sinsisidir: eğitimde model sağdaki kelimeye bakıp kopyalar,
kayıp sıfıra yaklaşır; üretimde sağda kelime olmadığı için hiçbir şey
üretemez.
