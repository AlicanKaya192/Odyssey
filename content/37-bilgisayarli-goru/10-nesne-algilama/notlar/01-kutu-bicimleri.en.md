| Format | Values | Where it appears |
|---|---|---|
| xyxy | top-left x, top-left y, bottom-right x, bottom-right y | torchvision (`box_iou`, `nms`), most drawing code |
| xywh | top-left x, top-left y, width, height | COCO dataset labels |
| cxcywh | centre x, centre y, width, height | The YOLO family (often divided by the picture size, 0–1) |

Going from one format to another and back must not damage the box:

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

- After the round trip the box is the same.
- The last line is the format of YOLO's label files: the centre and the sizes
  divided by the picture's width and height (here the picture is 32 × 32).
  Since it does not depend on the picture size, the label does not change when
  the picture is enlarged; but it must be multiplied by the picture size
  before use.
- You cannot always tell a box's format by looking at the numbers
  (`[4, 6, 10, 6]` could be xywh or a broken xyxy); check the documentation.
