import torch
import torch.nn.functional as F


def objectness_loss(logits, target):
    return 0.0

print(objectness_loss([[2.0, -2.0], [-2.0, -2.0]], [[1, 0], [0, 0]]))
print(objectness_loss([[0.0, 0.0], [0.0, 0.0]], [[1, 0], [0, 0]]))
