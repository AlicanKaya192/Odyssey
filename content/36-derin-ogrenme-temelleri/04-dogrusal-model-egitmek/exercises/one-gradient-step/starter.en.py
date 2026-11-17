import torch


def one_step(w_value, b_value, xs, ys, lr):
    w = torch.tensor(w_value, requires_grad=True)
    b = torch.tensor(b_value, requires_grad=True)
    x, y = torch.tensor(xs), torch.tensor(ys)
    return [w.item(), b.item()]

print(one_step(0.0, 0.0, [1.0, 2.0], [3.0, 5.0], 0.1))
print(one_step(1.0, 1.0, [1.0], [2.0], 0.5))
