import torch


def fit_line(xs, ys):
    x, y = torch.tensor(xs), torch.tensor(ys)
    A = torch.stack([x, torch.ones_like(x)], dim=1)
    w, b = torch.linalg.lstsq(A, y.unsqueeze(1)).solution.flatten().tolist()
    return [round(w, 3), round(b, 3)]

print(fit_line([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0]))
print(fit_line([1.0, 2.0, 4.0], [-0.5, -1.5, -3.5]))
