from torch import nn


def conv_params(in_channels, out_channels, kernel):
    conv = nn.Conv1d(in_channels, out_channels, kernel)
    return sum(p.numel() for p in conv.parameters())

print(conv_params(1, 4, 5))
print(conv_params(8, 8, 5))
