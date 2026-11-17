import torch


def vector_grad(w_values, x_values):
    w = torch.tensor(w_values, requires_grad=True)
    x = torch.tensor(x_values)
    loss = (w * x).sum() + (w ** 2).sum()
    loss.backward()
    return w.grad.tolist()

print(vector_grad([1.0, 2.0, 3.0], [0.5, -1.0, 2.0]))
