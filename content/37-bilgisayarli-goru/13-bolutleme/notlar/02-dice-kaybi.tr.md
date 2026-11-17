IoU ile Dice aynı iki sayıdan (ortak alan, iki kümenin alanı) hesaplanıyor;
biri bilinince öteki de bilinir: Dice = 2 × IoU / (1 + IoU).

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

Bir satır kaymış 4 × 4'lük kare: 12 ortak piksel, IoU 0,6, Dice 0,75.

**Dice kaybı** bu ölçüyü doğrudan eğitime koyar. Tahmin 0/1 değil olasılık
olduğu için "yumuşak" sürümü kullanılır: ortak alan yerine olasılık × hedef
toplamı.

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

- Kusursuz tahminde kayıp 0, bir satır kaymışta 0,24, her yere 0,5 diyende
  0,65.
- `eps` boş maskede (hedef de tahmin de sıfır) sıfıra bölmeyi önlüyor.
- Dice kaybı yalnızca o sınıfın piksellerine baktığı için arka planın
  kalabalığından etkilenmiyor; çoğu zaman çapraz entropiyle toplanarak
  kullanılır.
