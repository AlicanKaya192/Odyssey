from collections import Counter


def ioc(text):
    n = len(text)
    counts = Counter(text)
    return round(sum(v * (v - 1) for v in counts.values()) / (n * (n - 1)), 4)

from cipher_data import SAMPLE

print(ioc(SAMPLE))
print(ioc("abcdefghijklmnopqrstuvwxyz"))
print(ioc("AAaa!"))
print(ioc("a"))
