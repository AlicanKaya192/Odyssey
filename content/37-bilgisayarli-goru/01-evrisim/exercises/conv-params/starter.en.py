from torch import nn


def conv_params(in_ch, out_ch, k):
    return 0

for in_ch, out_ch, k in [(1, 8, 3), (3, 16, 3), (16, 32, 5)]:
    layer = nn.Conv2d(in_ch, out_ch, k)
    real = sum(p.numel() for p in layer.parameters())
    print(in_ch, out_ch, k, conv_params(in_ch, out_ch, k), real)
