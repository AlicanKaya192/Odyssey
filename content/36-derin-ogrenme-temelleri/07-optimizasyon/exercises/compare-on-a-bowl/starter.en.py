import torch


def bowl(w):
    return 20 * w[0] ** 2 + w[1] ** 2


def run(make_optimizer, steps=40):
    w = torch.tensor([1.0, 2.0], dtype=torch.float64, requires_grad=True)
    optimizer = make_optimizer([w])
    # 40 steps: zero_grad, backward, step
    return round(bowl(w).item(), 3)


print("SGD", run(lambda p: torch.optim.SGD(p, lr=0.02)))
print("momentum", run(lambda p: torch.optim.SGD(p, lr=0.02, momentum=0.9)))
print("Adam", run(lambda p: torch.optim.Adam(p, lr=0.1)))
