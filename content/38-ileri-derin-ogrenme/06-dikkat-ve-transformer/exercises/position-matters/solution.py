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
    with torch.no_grad():
        plain = torch.allclose(encoder(x)[:, perm], encoder(x[:, perm]), atol=1e-5)
        with_pos = encoder(x + pos.weight)
        with_pos_perm = encoder(x[:, perm] + pos.weight)
        positioned = torch.allclose(with_pos[:, perm], with_pos_perm, atol=1e-5)
    return [plain, positioned]

print(position_matters(5))
print(position_matters(3))
