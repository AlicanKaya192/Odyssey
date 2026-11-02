from collections import Counter


def ioc(text):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    return round(sum(v * (v - 1) for v in counts.values()) / (n * (n - 1)), 4)

from cipher_data import SAMPLE

print(ioc(SAMPLE))
print(ioc("abcdefghijklmnopqrstuvwxyz"))
print(ioc("AAaa!"))
print(ioc("a"))
