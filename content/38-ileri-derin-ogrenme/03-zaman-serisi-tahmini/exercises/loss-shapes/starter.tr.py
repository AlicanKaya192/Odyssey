import torch


def loss_shapes(batch):
    pred = torch.zeros(batch, 1)
    target = torch.zeros(batch)
    # Kodunu buraya yaz
    return []

print(loss_shapes(4))
print(loss_shapes(1))
