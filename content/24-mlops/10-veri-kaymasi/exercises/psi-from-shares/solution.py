import math


def psi_from_shares(reference, current):
    total = 0
    for r, c in zip(reference, current):
        r, c = max(r, 0.0001), max(c, 0.0001)
        total += (c - r) * math.log(c / r)
    return round(total, 3)


reference = [0.25, 0.25, 0.25, 0.25]
print(psi_from_shares(reference, reference))
print(psi_from_shares(reference, [0.4, 0.3, 0.2, 0.1]))
print(psi_from_shares(reference, [0.5, 0.5, 0.0, 0.0]))
