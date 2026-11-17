import torch
import torch.nn.functional as F
from torch import nn


class DownBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        # Shortcut: a 1 x 1 convolution (stride 2) and BatchNorm that bring x to out's shape.
        self.shortcut = nn.Identity()

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return F.relu(out + self.shortcut(x))


block = DownBlock(16, 32)
print(tuple(block(torch.zeros(2, 16, 8, 8)).shape))
print(sum(p.numel() for p in block.shortcut.parameters()))
