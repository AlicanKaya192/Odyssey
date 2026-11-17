import torch


def totals(rows):
    t = torch.tensor(rows)
    return [t.sum(dim=1).tolist(), t.sum(dim=0).tolist()]

print(totals([[1, 2, 3], [4, 5, 6]]))
print(totals([[10, 0], [0, 10], [5, 5]]))
