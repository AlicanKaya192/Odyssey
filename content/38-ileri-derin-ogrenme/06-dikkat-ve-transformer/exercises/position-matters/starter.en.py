import torch
from torch import nn


def position_matters(length):
    torch.manual_seed(0)
    layer = nn.TransformerEncoderLayer(8, nhead=2, dim_feedforward=16,
                                       dropout=0.0, batch_first=True)
    encoder = nn.TransformerEncoder(layer, num_layers=1)
    encoder.eval()
    pos = nn.Embedding(length, 8)
    x = torch.randn(1, length, 8)
    perm = torch.arange(length).flip(0)
    # Write your code here
    return []

print(position_matters(5))
print(position_matters(3))
