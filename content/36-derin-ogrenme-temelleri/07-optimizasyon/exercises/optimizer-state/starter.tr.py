import torch

MAKERS = {
    "sgd": lambda p: torch.optim.SGD(p, lr=0.1),
    "momentum": lambda p: torch.optim.SGD(p, lr=0.1, momentum=0.9),
    "adam": lambda p: torch.optim.Adam(p, lr=0.1),
}


def state_names(kind):
    w = torch.ones(3, requires_grad=True)
    optimizer = MAKERS[kind]([w])
    return []

for kind in ["sgd", "momentum", "adam"]:
    print(kind, state_names(kind))
