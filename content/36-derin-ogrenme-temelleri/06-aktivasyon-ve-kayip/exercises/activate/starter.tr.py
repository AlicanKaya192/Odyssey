import torch


def activate(values, name):
    return values

values = [-2.0, 0.0, 1.0]
for name in ["relu", "sigmoid", "tanh"]:
    print(name, activate(values, name))
