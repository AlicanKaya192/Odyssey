import torch


def mse(pred, target):
    pred, target = torch.tensor(pred), torch.tensor(target)
    return round(((pred - target) ** 2).mean().item(), 4)

print(mse([1.0, 2.0, 3.0], [1.0, 2.0, 5.0]))
print(mse([0.0, 0.0], [3.0, -1.0]))
