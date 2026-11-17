import torch


def info(rows):
    t = torch.tensor(rows)
    return [list(t.shape), str(t.dtype)]

print(info([[1, 2, 3], [4, 5, 6]]))
print(info([1.5, 2.5]))
