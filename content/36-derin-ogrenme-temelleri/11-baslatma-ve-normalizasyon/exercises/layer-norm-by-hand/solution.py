import torch
from torch import nn


def layer_norm(rows):
    x = torch.tensor(rows)
    mean = x.mean(dim=1, keepdim=True)
    var = x.var(dim=1, unbiased=False, keepdim=True)
    out = (x - mean) / torch.sqrt(var + 1e-5)
    assert torch.allclose(out, nn.LayerNorm(x.shape[1])(x), atol=1e-5)
    return [[round(v, 2) for v in row] for row in out.tolist()]

print(layer_norm([[1.0, 2.0, 3.0], [10.0, 10.0, 40.0]]))
