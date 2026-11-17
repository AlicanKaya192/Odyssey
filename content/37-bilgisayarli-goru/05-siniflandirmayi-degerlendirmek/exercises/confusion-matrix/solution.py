import torch


def confusion(y_true, y_pred, k):
    t = torch.tensor(y_true)
    p = torch.tensor(y_pred)
    return torch.bincount(t * k + p, minlength=k * k).reshape(k, k).tolist()

for row in confusion([0, 0, 1, 1, 2, 2], [0, 1, 1, 1, 2, 0], 3):
    print(row)
