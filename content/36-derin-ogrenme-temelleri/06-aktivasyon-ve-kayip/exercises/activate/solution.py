import torch

FUNCTIONS = {"relu": torch.relu, "sigmoid": torch.sigmoid, "tanh": torch.tanh}


def activate(values, name):
    out = FUNCTIONS[name](torch.tensor(values))
    return [round(v, 3) for v in out.tolist()]

values = [-2.0, 0.0, 1.0]
for name in ["relu", "sigmoid", "tanh"]:
    print(name, activate(values, name))
