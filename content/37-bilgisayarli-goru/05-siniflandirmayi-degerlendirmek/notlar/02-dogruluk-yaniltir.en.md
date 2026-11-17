When classes are imbalanced, accuracy misleads. Picture a production line
where 5 of 100 pictures show a defect. A model that always says "no defect"
without looking at anything:

```python
import torch

y = torch.tensor([1] * 5 + [0] * 95)
always_no = torch.zeros(100, dtype=torch.long)
accuracy = (always_no == y).float().mean().item()
found = ((always_no == 1) & (y == 1)).sum().item()
recall = found / (y == 1).sum().item()
print(round(accuracy, 2), recall)
```

```text
0.95 0.0
```

95% accuracy, yet it finds none of the five defects we are looking for (recall
0). In such a problem:

- The rare class's **recall**, **precision** and **F1** are reported; accuracy
  is never given alone.
- The confusion matrix is always checked.
- Giving the loss class weights (`nn.CrossEntropyLoss(weight=...)`) or sampling
  the rare class more often (`WeightedRandomSampler`) can help in training.

The shape and digit data of this module are balanced; imbalance returns in
the object detection and segmentation sections (most of a picture is
background).
