from collections import Counter


def cohen_kappa(a, b):
    observed = sum(x == y for x, y in zip(a, b)) / len(a)
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in ca) / len(a) ** 2
    if expected == 1:
        return 1.0
    return round((observed - expected) / (1 - expected), 3)

a = ["pos", "pos", "neg", "neg", "pos", "neu"]
b = ["pos", "neg", "neg", "neg", "pos", "pos"]
print(cohen_kappa(a, b))
print(cohen_kappa(a, a))
