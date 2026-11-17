import torch


def f(t):
    return 3 * t ** 2 + t


def compare(value):
    return [0.0, 0.0]

print(compare(1.5))
print(compare(-2.0))
