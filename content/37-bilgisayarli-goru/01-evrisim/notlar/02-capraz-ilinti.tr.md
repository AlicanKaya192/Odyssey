Matematik ve sinyal işleme derslerinde "evrişim" çekirdeği önce iki yönde
ters çevirir, sonra çarpıp toplar. `F.conv2d` çevirmiyor: yaptığı
**çapraz ilinti** (cross-correlation). Farkı küçük bir örnekte görelim:

```python
import torch
import torch.nn.functional as F

x = torch.arange(16.0).reshape(1, 1, 4, 4)
k = torch.tensor([[1.0, 2.0], [3.0, 4.0]]).reshape(1, 1, 2, 2)
cross = F.conv2d(x, k)
flipped = torch.flip(k, dims=[2, 3])
true_conv = F.conv2d(x, flipped)
print(cross[0, 0].tolist())
print(true_conv[0, 0].tolist())
```

```text
[[34.0, 44.0, 54.0], [74.0, 84.0, 94.0], [114.0, 124.0, 134.0]]
[[16.0, 26.0, 36.0], [56.0, 66.0, 76.0], [96.0, 106.0, 116.0]]
```

- Aynı çekirdekle iki işlem farklı sayılar veriyor.
- Gerçek evrişimi istersen çekirdeği `torch.flip` ile çevirip `F.conv2d`'ye
  vermen yeterli.
- Ağda bu fark önemsiz: çekirdek öğreniliyor. Ağ çevrilmiş bir deseni
  istiyorsa sayıları zaten çevrilmiş hâliyle öğrenir.

Hazır bir kenar çekirdeğini (Sobel gibi) bir kitaptan alıp elle uygularken bu
fark işaretin ters çıkmasına yol açabilir; sonucu bir örnekle sınamak iyi
alışkanlık.
