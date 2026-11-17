Every library describes the same picture in a different order. When you see a
shape error, this table is the first place to look.

| Where | Order | A colour picture with 3 rows, 5 columns |
|---|---|---|
| Pillow `size` | width, height | `(5, 3)` |
| NumPy `shape` | height, width, channel | `(3, 5, 3)` |
| PyTorch single image | channel, height, width | `(3, 3, 5)` |
| PyTorch batch | image, channel, height, width | `(1, 3, 3, 5)` |
| matplotlib `imshow` | height, width, channel | `(3, 5, 3)` |

Going from one to the other:

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

- `unsqueeze(0)` adds an axis of size 1 at the front: it turns a single
  picture into a batch. Networks always expect a batch, so this step must not
  be forgotten when predicting on one picture.
- Before drawing with matplotlib we move the channel back to the end:
  `permute(1, 2, 0)`.
- In a grey picture the channel dimension is 1: `(1, H, W)`. `squeeze(0)`
  drops it.
