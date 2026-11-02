import math


def rule_of_16(sd, delta):
    return math.ceil(16 * sd / delta)


print(rule_of_16(0.32, 0.006))
print(rule_of_16(48.0, 0.6))
