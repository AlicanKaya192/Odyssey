| Biçim | Değerler | Nerede görülür |
|---|---|---|
| xyxy | sol üst x, sol üst y, sağ alt x, sağ alt y | torchvision (`box_iou`, `nms`), çoğu çizim kodu |
| xywh | sol üst x, sol üst y, genişlik, yükseklik | COCO veri seti etiketleri |
| cxcywh | merkez x, merkez y, genişlik, yükseklik | YOLO ailesi (çoğu zaman resim boyuna bölünmüş, 0–1) |

Bir biçimden ötekine gidip geri gelmek kutuyu bozmamalı:

```python
import torch
from torchvision.ops import box_convert

box = torch.tensor([[4.0, 6.0, 14.0, 12.0]])
for fmt in ("xywh", "cxcywh"):
    there = box_convert(box, "xyxy", fmt)
    back = box_convert(there, fmt, "xyxy")
    print(fmt, there.tolist(), torch.equal(back, box))

normalized = box_convert(box, "xyxy", "cxcywh") / 32
print(normalized.tolist())
```

```text
xywh [[4.0, 6.0, 10.0, 6.0]] True
cxcywh [[9.0, 9.0, 10.0, 6.0]] True
[[0.28125, 0.28125, 0.3125, 0.1875]]
```

- Gidip gelince kutu aynı kalıyor.
- Son satır YOLO'nun etiket dosyalarındaki biçim: merkez ve boyutlar resmin
  genişliği ve yüksekliğiyle bölünmüş (burada resim 32 × 32). Resim boyundan
  bağımsız olduğu için resim büyüyünce etiket değişmiyor; ama kullanmadan
  önce resim boyuyla çarpmak gerekiyor.
- Bir kutunun hangi biçimde olduğunu sayılara bakarak anlamak her zaman
  mümkün değil (`[4, 6, 10, 6]` hem xywh hem bozuk bir xyxy olabilir);
  belgeye bak.
