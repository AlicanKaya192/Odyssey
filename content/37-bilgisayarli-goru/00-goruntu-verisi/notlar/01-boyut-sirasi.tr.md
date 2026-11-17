Aynı resmi her kütüphane başka bir sırayla anlatıyor. Bir şekil hatası
gördüğünde ilk bakacağın yer bu tablo.

| Nerede | Sıra | 3 satır, 5 sütunluk renkli resim |
|---|---|---|
| Pillow `size` | genişlik, yükseklik | `(5, 3)` |
| NumPy `shape` | yükseklik, genişlik, kanal | `(3, 5, 3)` |
| PyTorch tek resim | kanal, yükseklik, genişlik | `(3, 3, 5)` |
| PyTorch yığın | resim, kanal, yükseklik, genişlik | `(1, 3, 3, 5)` |
| matplotlib `imshow` | yükseklik, genişlik, kanal | `(3, 5, 3)` |

Bir yönden ötekine geçiş:

```python
import numpy as np
import torch
from PIL import Image

picture = Image.new("RGB", (5, 3))
array = np.array(picture)
tensor = torch.from_numpy(array).permute(2, 0, 1)
batch = tensor.unsqueeze(0)
back = batch[0].permute(1, 2, 0).numpy()
print(picture.size)
print(array.shape)
print(tuple(tensor.shape))
print(tuple(batch.shape))
print(back.shape)
```

```text
(5, 3)
(3, 5, 3)
(3, 3, 5)
(1, 3, 3, 5)
(3, 5, 3)
```

- `unsqueeze(0)` başa 1 boyutlu bir eksen ekliyor: tek resmi bir yığına
  çeviriyor. Ağlar hep yığın beklediği için tek resimle tahmin yaparken bu
  adım unutulmaz.
- matplotlib'e çizdirmeden önce kanalı yeniden sona alıyoruz:
  `permute(1, 2, 0)`.
- Gri resimde kanal boyutu 1'dir: `(1, H, W)`. `squeeze(0)` onu atar.
