**Tracking** a person from frame to frame in a video (always giving the same
person the same number) is also a matching problem: match the boxes in this
frame with those in the previous frame. Each box must match at most once and
the total must be the best: exactly the job of the Hungarian algorithm.

```python
import torch
from scipy.optimize import linear_sum_assignment
from torchvision.ops import box_iou

previous = {7: [10.0, 10, 20, 30], 8: [40, 12, 50, 32]}
current = torch.tensor([[42.0, 13, 52, 33], [12, 11, 22, 31], [70, 10, 80, 30]])
ids = list(previous)
ious = box_iou(current, torch.tensor(list(previous.values())))
rows, cols = linear_sum_assignment(-ious.numpy())
next_id = max(ids) + 1
assigned = {}
for r, c in zip(rows, cols):
    if ious[r, c] >= 0.3:
        assigned[int(r)] = ids[c]
for r in range(len(current)):
    if r not in assigned:
        assigned[r] = next_id
        next_id += 1
print([assigned[r] for r in range(len(current))])
```

```text
[8, 7, 9]
```

- The first box in this frame is close to person 8 of the previous frame, the
  second to 7: the numbers are kept (even though the order changed).
- The third box overlaps no old box: a new person, a new number (9).
- In tracking the threshold is usually lower than in detection (here 0.3):
  a person moves a little between two frames.

Real tracking systems add motion prediction (where the person will be in the
next frame) and appearance similarity (the embeddings of the earlier
section); the heart of the matching is still the same assignment problem.
