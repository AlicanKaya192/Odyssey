from torch import nn


def trainable_last(hidden):
    net = nn.Sequential(nn.Linear(6, hidden), nn.ReLU(), nn.Linear(hidden, 3))
    # Freeze everything, open only the last layer; return the trainable count
    return sum(p.numel() for p in net.parameters())

print(trainable_last(64))
print(trainable_last(8))
