Training and testing get **two separate** transform chains. The only shared
steps are the ones that prepare the picture for the network (type,
normalisation); random augmentation is for training only.

```python
import torch
from torchvision.transforms import v2

mean, std = 0.2, 0.3
train_tf = v2.Compose([
    v2.RandomHorizontalFlip(),
    v2.RandomCrop(16, padding=3),
    v2.Normalize([mean], [std]),
])
test_tf = v2.Normalize([mean], [std])

img = torch.full((1, 16, 16), 0.5)
torch.manual_seed(0)
print(torch.equal(test_tf(img), test_tf(img)))
print(round(test_tf(img).min().item(), 3), round(train_tf(img).min().item(), 3))
```

```text
True
1.0 -0.667
```

- The test transform gives the same result every time: the measurement is
  repeatable.
- The crop in the training transform brings the padding's zeros into the
  picture too (−0.667 after normalisation). The network sees these edges in
  training and not in testing. That is fine: augmentation is there to make
  training harder and generalisation better.
- `mean` and `std` are computed once from the training data, and **the same
  numbers are used in both chains**.

| | Training | Validation / test |
|---|---|---|
| Random flip, crop, rotation | Yes | No |
| `ToDtype`, `Normalize` | Yes | Yes (same numbers) |
| `DataLoader(shuffle=...)` | `True` | `False` |
