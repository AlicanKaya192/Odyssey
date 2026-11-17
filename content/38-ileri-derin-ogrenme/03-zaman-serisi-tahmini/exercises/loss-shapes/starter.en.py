import torch


def loss_shapes(batch):
    pred = torch.zeros(batch, 1)
    target = torch.zeros(batch)
    # Write your code here
    return []

print(loss_shapes(4))
print(loss_shapes(1))
