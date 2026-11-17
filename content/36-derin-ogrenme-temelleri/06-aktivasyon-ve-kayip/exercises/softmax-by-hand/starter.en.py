import torch


def to_probabilities(logits):
    z = torch.tensor(logits)
    return z.tolist()

print(to_probabilities([[2.0, 1.0, 0.1]]))
print(to_probabilities([[0.0, 0.0], [3.0, -3.0]]))
