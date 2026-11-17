Let us compute every measure by hand on a small three-class example and
compare it with scikit-learn.

| Measure | Question | From the matrix |
|---|---|---|
| Precision | How many of my "c" answers are c? | diagonal ÷ column sum |
| Recall | How many of the real c's did I find? | diagonal ÷ row sum |
| F1 | Are both good? | `2 · p · r / (p + r)` |

```python
import torch
from sklearn.metrics import f1_score

y_true = torch.tensor([0, 0, 0, 0, 0, 0, 1, 1, 2, 2])
y_pred = torch.tensor([0, 0, 0, 0, 0, 1, 1, 0, 2, 1])
counts = torch.bincount(y_true * 3 + y_pred, minlength=9).reshape(3, 3)
correct = counts.diag().float()
precision = correct / counts.sum(dim=0)
recall = correct / counts.sum(dim=1)
f1 = 2 * precision * recall / (precision + recall)
print(counts.tolist())
print([round(v, 3) for v in precision.tolist()])
print([round(v, 3) for v in recall.tolist()])
print(round(f1.mean().item(), 3), round(f1_score(y_true, y_pred, average="macro"), 3))
print(round(f1_score(y_true, y_pred, average="weighted"), 3))
```

```text
[[5, 1, 0], [1, 1, 0], [0, 1, 1]]
[0.833, 0.333, 1.0]
[0.833, 0.5, 0.5]
0.633 0.633
0.713
```

- The mean of the hand-computed F1 scores is the same as scikit-learn's
  `macro` F1.
- The `weighted` F1 is higher: class 0, with six examples, was predicted well
  and counts more in the weighted mean. To see failure in small classes,
  look at `macro`.
- If a class is never predicted, its column sum is 0 and precision becomes
  `0 / 0` (`nan`). scikit-learn warns and writes 0 in that case.
