import torch


def step_size(optimizer_class, scale):
    w = torch.tensor(1.0, requires_grad=True)
    optimizer = optimizer_class([w], lr=0.1)
    (scale * w ** 2).backward()
    optimizer.step()
    return round(1.0 - w.item(), 4)


def first_step(scale):
    return [step_size(torch.optim.SGD, scale), step_size(torch.optim.Adam, scale)]

for scale in [0.01, 1.0, 100.0]:
    print(scale, first_step(scale))
