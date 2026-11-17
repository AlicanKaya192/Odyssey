import math

from torch import nn


def expected_std(fan_in, nonlinearity):
    gain = nn.init.calculate_gain(nonlinearity)
    return round(gain / math.sqrt(fan_in), 4)

print(expected_std(256, "relu"))
print(expected_std(100, "tanh"))
