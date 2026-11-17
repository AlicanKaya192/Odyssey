import torch
import torch.nn.functional as F


def precision_at_k(vectors, labels, k):
    unit = F.normalize(torch.tensor(vectors), dim=1)
    scores = unit @ unit.T
    scores.fill_diagonal_(-2)
    nearest = scores.topk(k, dim=1).indices
    y = torch.tensor(labels)
    return round((y[nearest] == y[:, None]).float().mean().item(), 3)

vectors = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [0.1, 0.9], [0.8, 0.6]]
labels = [0, 0, 1, 1, 0]
print(precision_at_k(vectors, labels, 1))
print(precision_at_k(vectors, labels, 2))
