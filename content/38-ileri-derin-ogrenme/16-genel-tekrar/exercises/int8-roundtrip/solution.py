import torch


def int8_roundtrip(values):
    w = torch.tensor(values)
    scale = w.abs().max() / 127
    q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
    return [round(v, 3) for v in (q.float() * scale).tolist()]

print(int8_roundtrip([1.27, -0.5, 0.0]))
