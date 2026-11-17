An augmentation only helps if it **does not change the picture's label**.
Rotating digits by 180 degrees breaks this: a 6 turned upside down looks like
a 9. Let us measure it with a simple classifier: we take the mean picture of
each digit and put every picture into the class of the nearest mean.

```python
import torch
from sklearn.datasets import load_digits

digits = load_digits()
x = torch.tensor(digits.images, dtype=torch.float32)
y = torch.tensor(digits.target)
means = torch.stack([x[y == d].mean(dim=0) for d in range(10)])


def nearest(images):
    distances = ((images[:, None] - means[None]) ** 2).sum(dim=(2, 3))
    return distances.argmin(dim=1)


sixes = x[y == 6]
print(len(sixes))
print(torch.bincount(nearest(sixes), minlength=10).tolist())
turned = torch.rot90(sixes, k=2, dims=(1, 2))
print(torch.bincount(nearest(turned), minlength=10).tolist())
```

```text
181
[1, 4, 0, 0, 0, 0, 175, 0, 1, 0]
[0, 16, 1, 6, 2, 2, 0, 4, 2, 148]
```

- 175 of the 181 sixes go to the right class (6).
- When the same pictures are rotated by 180 degrees, 148 go to class 9; none
  stays a 6. Training with the label "rotated 6" would teach the network
  something wrong.

Which augmentation is safe depends on the task and the data:

| Data | Safe | May break the label |
|---|---|---|
| Digits, letters | Small shifts, small rotations | Mirroring, 180° rotation (6 ↔ 9, b ↔ d) |
| The shapes in this module | Horizontal mirroring, shifts | Vertical mirroring (the triangle turns over) |
| Natural photos (cats, dogs) | Horizontal mirroring, crops, colour jitter | Vertical mirroring (upside-down dogs do not occur) |
| Object detection | Transforms applied together with the box | Cropping without updating the box |

Rule: look at the augmented picture and ask "does this still deserve the same
label?"
