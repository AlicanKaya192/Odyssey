from torch import nn


def mha_params(dim, heads):
    attn = nn.MultiheadAttention(dim, heads, batch_first=True)
    return sum(p.numel() for p in attn.parameters())

print(mha_params(8, 2))
print(mha_params(8, 4))
print(mha_params(64, 8))
