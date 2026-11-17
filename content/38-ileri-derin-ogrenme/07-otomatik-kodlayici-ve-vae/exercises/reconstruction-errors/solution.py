import torch


def reconstruction_errors(original, rebuilt):
    a, b = torch.tensor(original), torch.tensor(rebuilt)
    return [round(v, 3) for v in ((a - b) ** 2).mean(dim=1).tolist()]

original = [[1.0, 0.0, 1.0, 0.0], [0.5, 0.5, 0.5, 0.5]]
rebuilt = [[1.0, 0.0, 0.0, 0.0], [0.5, 0.5, 0.5, 0.5]]
print(reconstruction_errors(original, rebuilt))
