Bir kutunun sağ alt köşesi son pikselin **kendisi** mi, yoksa bir
**fazlası** mı? İki gelenek de var ve karıştırmak alanı ve IoU'yu sessizce
değiştirir. `make_scenes` ikincisini kullanıyor: `x2` son sütunun bir
fazlası. Bunu maskeyle doğrulayalım:

```python
import numpy as np
from dl_data import make_scenes

images, boxes, masks = make_scenes(100, size=32, seed=7)
x1, y1, x2, y2, label = boxes[0][0]
ys, xs = np.nonzero(masks[0] == label + 1)
print(xs.min(), xs.max(), x1, x2)
print(ys.min(), ys.max(), y1, y2)
print((x2 - x1) * (y2 - y1))
print((xs.max() - xs.min()) * (ys.max() - ys.min()))
```

```text
17 25 17 26
7 15 7 16
81
64
```

- Şeklin en sağdaki pikseli 25. sütunda, `x2` ise 26: bir fazlası. `y2`
  için de aynı.
- Bu gelenekte genişlik doğrudan `x2 − x1` (9 piksel) ve alan 81.
- Biri aynı kutuyu "son piksel dahil" yazıp (`x2 = 25`) alanı yine
  `x2 − x1` ile hesaplarsa 64 bulur: her kenardan bir piksel kayıp. Küçük
  nesnelerde bu fark IoU'yu belirgin değiştirir.

torchvision'ın kutu fonksiyonları sürekli koordinat varsayar: `x2 − x1`
genişliktir. Kendi veri setinin geleneğini bir kez doğrula, sonra bütün
kodda aynı kalsın.
