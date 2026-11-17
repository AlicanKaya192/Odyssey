import torch


def top(scores):
    values, indices = torch.tensor(scores).max(dim=1)
    return [values.tolist(), indices.tolist()]

scores = [[0.5, 2.0, 1.0], [3.0, 0.25, 0.75], [1.0, 1.5, 4.0]]
print(top(scores))
