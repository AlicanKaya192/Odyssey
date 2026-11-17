from torch import nn


def trainable_last(hidden):
    net = nn.Sequential(nn.Linear(6, hidden), nn.ReLU(), nn.Linear(hidden, 3))
    net.requires_grad_(False)
    net[-1].requires_grad_(True)
    return sum(p.numel() for p in net.parameters() if p.requires_grad)

print(trainable_last(64))
print(trainable_last(8))
