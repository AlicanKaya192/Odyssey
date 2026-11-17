import torch


def loss_shapes(batch):
    pred = torch.zeros(batch, 1)
    target = torch.zeros(batch)
    wrong = list((pred - target).shape)
    right = list((pred.squeeze(-1) - target).shape)
    return [wrong, right]

print(loss_shapes(4))
print(loss_shapes(1))
