import torch


def quantize_int8(values):
    w = torch.tensor(values)
    scale = w.abs().max() / 127
    q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
    return [q.tolist(), round(scale.item(), 4)]

print(quantize_int8([0.5, -1.27, 0.01]))
