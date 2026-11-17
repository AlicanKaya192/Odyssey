AP is computed at an **IoU threshold**: the overlap a prediction needs to count
as right. The same predictions become less "right" as the threshold rises:

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

- The predictions are already in score order and each is close to a different
  true box; so the best IoU is enough instead of matching.
- At IoU 0.5 two predictions are right, AP 0.667. At IoU 0.75 only the first
  prediction (IoU 0.82) is good enough; AP 0.333.

Common names:

| Name | Meaning |
|---|---|
| AP@0.5 (AP50) | AP at an IoU threshold of 0.5 |
| AP@0.75 | AP at an IoU threshold of 0.75; rewards a precisely placed box |
| mAP | The mean of the classes' APs (each class computed separately) |
| mAP@[.5:.95] | The mean of mAP over ten IoU thresholds from 0.5 to 0.95 in steps of 0.05 (the COCO measure) |

When you see "mAP" in a paper or a library's output, check at which IoU
threshold it is; for the same model the numbers differ a lot.
