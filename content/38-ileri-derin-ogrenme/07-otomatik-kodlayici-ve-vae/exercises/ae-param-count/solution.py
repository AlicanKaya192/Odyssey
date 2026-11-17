from torch import nn


def ae_param_count(code):
    encoder = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, code))
    decoder = nn.Sequential(nn.Linear(code, 32), nn.ReLU(), nn.Linear(32, 64), nn.Sigmoid())
    return sum(p.numel() for m in (encoder, decoder) for p in m.parameters())

print(ae_param_count(4))
print(ae_param_count(2))
