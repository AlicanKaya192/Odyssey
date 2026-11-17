import torch
import torch.nn.functional as F


def objectness_loss(logits, target):
    a = torch.tensor(logits, dtype=torch.float32)
    b = torch.tensor(target, dtype=torch.float32)
    return round(F.binary_cross_entropy_with_logits(a, b).item(), 3)

print(objectness_loss([[2.0, -2.0], [-2.0, -2.0]], [[1, 0], [0, 0]]))
print(objectness_loss([[0.0, 0.0], [0.0, 0.0]], [[1, 0], [0, 0]]))
