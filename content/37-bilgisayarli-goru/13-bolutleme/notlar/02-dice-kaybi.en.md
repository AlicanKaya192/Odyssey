IoU and Dice are computed from the same two numbers (the common area, the
areas of the two sets); knowing one gives the other: Dice = 2 × IoU /
(1 + IoU).

```python
import torch

truth = torch.zeros(8, 8, dtype=torch.bool)
truth[2:6, 2:6] = True
predicted = torch.zeros(8, 8, dtype=torch.bool)
predicted[3:7, 2:6] = True
common = (truth & predicted).sum().item()
iou = common / (truth | predicted).sum().item()
dice = 2 * common / (truth.sum().item() + predicted.sum().item())
print(common, round(iou, 3), round(dice, 3), round(2 * iou / (1 + iou), 3))
```

```text
12 0.6 0.75 0.75
```

A 4 × 4 square shifted by one row: 12 common pixels, IoU 0.6, Dice 0.75.

**Dice loss** puts this measure straight into training. Since the prediction
is a probability, not 0/1, its "soft" version is used: the sum of
probability × target instead of the common area.

```python
def soft_dice_loss(probabilities, target, eps=1.0):
    common = (probabilities * target).sum()
    total = probabilities.sum() + target.sum()
    return 1 - (2 * common + eps) / (total + eps)


target = truth.float()
print(round(soft_dice_loss(target, target).item(), 3))
print(round(soft_dice_loss(predicted.float(), target).item(), 3))
print(round(soft_dice_loss(torch.full((8, 8), 0.5), target).item(), 3))
```

```text
0.0
0.242
0.653
```

- The loss is 0 for a perfect prediction, 0.24 for one shifted by a row and
  0.65 for one that says 0.5 everywhere.
- `eps` prevents division by zero on an empty mask (both target and
  prediction zero).
- Because Dice loss looks only at the pixels of that class, it is not
  affected by the crowd of background pixels; it is often used added to
  cross-entropy.
