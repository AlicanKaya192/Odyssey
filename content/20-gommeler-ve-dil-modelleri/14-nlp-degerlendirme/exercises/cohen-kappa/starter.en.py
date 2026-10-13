from collections import Counter


def cohen_kappa(a, b):
    return 0.0

a = ["pos", "pos", "neg", "neg", "pos", "neu"]
b = ["pos", "neg", "neg", "neg", "pos", "pos"]
print(cohen_kappa(a, b))
print(cohen_kappa(a, a))
