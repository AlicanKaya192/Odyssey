import torch


def one_step(w_value, b_value, xs, ys, lr):
    w = torch.tensor(w_value, requires_grad=True)
    b = torch.tensor(b_value, requires_grad=True)
    x, y = torch.tensor(xs), torch.tensor(ys)
    loss = ((w * x + b - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    return [round(w.item(), 4), round(b.item(), 4)]

print(one_step(0.0, 0.0, [1.0, 2.0], [3.0, 5.0], 0.1))
print(one_step(1.0, 1.0, [1.0], [2.0], 0.5))
