import math


def psi_from_shares(reference, current):
    # Floor, term, sum.
    pass


reference = [0.25, 0.25, 0.25, 0.25]
print(psi_from_shares(reference, reference))
print(psi_from_shares(reference, [0.4, 0.3, 0.2, 0.1]))
print(psi_from_shares(reference, [0.5, 0.5, 0.0, 0.0]))
