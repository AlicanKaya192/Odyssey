AP, bir **IoU eşiğinde** hesaplanır: bir tahminin doğru sayılması için
gereken örtüşme. Aynı tahminler, eşik yükselince daha az "doğru" olur:

```python
import torch
from torchvision.ops import box_iou

truth = torch.tensor([[0.0, 0, 10, 10], [20, 20, 30, 30], [40, 0, 50, 10]])
preds = torch.tensor([[1.0, 0, 11, 10], [21, 22, 31, 32],
                      [44, 2, 54, 12], [60, 60, 70, 70]])
best = box_iou(preds, truth).max(dim=1).values
print([round(v, 2) for v in best.tolist()])


def average_precision(hits, total_truth):
    tp = hits.cumsum(0)
    precision = tp / torch.arange(1, len(hits) + 1)
    recall = tp / total_truth
    envelope = precision.flip(0).cummax(0).values.flip(0)
    steps = torch.cat([torch.tensor([0.0]), recall])
    return ((steps[1:] - steps[:-1]) * envelope).sum().item()


for threshold in (0.5, 0.75):
    hits = (best >= threshold).float()
    print(threshold, round(average_precision(hits, 3), 3))
```

```text
[0.82, 0.56, 0.32, 0.0]
0.5 0.667
0.75 0.333
```

- Tahminler zaten puan sırasında ve her biri ayrı bir gerçek kutuya
  yakın; bu yüzden eşleştirme yerine en iyi IoU yetiyor.
- IoU 0,5'te iki tahmin doğru, AP 0,667. IoU 0,75'te yalnızca ilk tahmin
  (IoU 0,82) yeterince iyi; AP 0,333.

Sık görülen adlar:

| Ad | Ne demek |
|---|---|
| AP@0.5 (AP50) | IoU eşiği 0,5'te AP |
| AP@0.75 | IoU eşiği 0,75'te AP; kutunun yerinin hassas olmasını ödüllendirir |
| mAP | Sınıfların AP'lerinin ortalaması (her sınıf ayrı hesaplanır) |
| mAP@[.5:.95] | 0,5'ten 0,95'e 0,05 adımla on IoU eşiğinde mAP'nin ortalaması (COCO ölçüsü) |

Bir makalede ya da kütüphane çıktısında "mAP" gördüğünde hangi IoU
eşiğinde olduğuna bak; aynı model için sayılar çok farklı çıkar.
