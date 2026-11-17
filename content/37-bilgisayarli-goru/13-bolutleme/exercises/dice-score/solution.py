import torch


def dice(predicted, truth, c):
    p = torch.tensor(predicted) == c
    t = torch.tensor(truth) == c
    total = p.sum().item() + t.sum().item()
    if total == 0:
        return 1.0
    return round(2 * (p & t).sum().item() / total, 3)

truth = [[0, 1, 1], [0, 1, 1], [0, 0, 0]]
print(dice([[0, 1, 1], [0, 1, 0], [0, 0, 0]], truth, 1))
print(dice([[0, 0, 0], [0, 0, 0], [0, 0, 0]], truth, 1))
print(dice(truth, truth, 2))
