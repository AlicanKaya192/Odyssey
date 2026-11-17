import math

from torch import nn


def expected_std(fan_in, nonlinearity):
    return 0.0

print(expected_std(256, "relu"))
print(expected_std(100, "tanh"))
