import torch


def row_scales(weight):
    w = torch.tensor(weight)
    return [round(v, 4) for v in (w.abs().amax(dim=1) / 127).tolist()]

print(row_scales([[0.127, -0.0635], [12.7, 1.0]]))
