In a YOLO with anchors every cell has several anchors; which anchor learns an
object? Usually **the one with the most similar shape**: the IoU between the
object's width and height and the anchor's, computed as if both boxes had the
same centre.

```python
import torch

anchors = torch.tensor([[8.0, 8.0], [8.0, 16.0], [16.0, 8.0]])
objects = torch.tensor([[7.0, 15.0], [14.0, 9.0], [9.0, 9.0]])


def shape_iou(a, b):
    inter = torch.minimum(a[:, None], b[None]).prod(dim=2)
    union = a.prod(dim=1)[:, None] + b.prod(dim=1)[None] - inter
    return inter / union


iou = shape_iou(objects, anchors)
print([[round(v, 2) for v in row] for row in iou.tolist()])
print(iou.argmax(dim=1).tolist())
```

```text
[[0.5, 0.82, 0.32], [0.51, 0.4, 0.79], [0.79, 0.53, 0.53]]
[1, 2, 0]
```

- The tall, narrow object (7 × 15) goes to the upright anchor (8 × 16), the
  wide, low object (14 × 9) to the lying anchor (16 × 8), the nearly square
  object (9 × 9) to the square anchor (8 × 8).
- `torch.minimum(a[:, None], b[None])` uses broadcasting to find the common
  width and height for every object–anchor pair; with the same centre the
  common area is their product.
- Anchor sizes are often chosen by clustering (k-means) the widths and heights
  of the boxes in the training data.

If two objects falling into the same cell go to different anchors, both can be
learned; that is one benefit of anchors.
