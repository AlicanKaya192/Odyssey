import torch
from torch import nn


class LoRALinear(nn.Module):
    def __init__(self, base, r=4, alpha=8):
        super().__init__()
        self.base = base.requires_grad_(False)
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale

def lora_report(r):
    torch.manual_seed(0)
    layer = nn.Linear(8, 4)
    lora = LoRALinear(layer, r=r)
    x = torch.randn(3, 8)
    same = torch.equal(lora(x), layer(x))
    trainable = sum(p.numel() for p in lora.parameters() if p.requires_grad)
    with torch.no_grad():
        lora.B.fill_(1.0)
    changed = not torch.equal(lora(x), layer(x))
    return [same, trainable, changed]


print(lora_report(2))
