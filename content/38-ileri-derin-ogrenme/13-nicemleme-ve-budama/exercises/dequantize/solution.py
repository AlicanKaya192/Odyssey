import torch


def dequantize(q, scale):
    restored = torch.tensor(q, dtype=torch.int8).float() * scale
    return [round(v, 3) for v in restored.tolist()]

print(dequantize([127, -64, 0], 0.01))
