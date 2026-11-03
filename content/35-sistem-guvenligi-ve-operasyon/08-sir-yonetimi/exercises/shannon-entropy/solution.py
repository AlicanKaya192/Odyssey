import math
from collections import Counter


def entropy(text):
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    value = -sum(c / total * math.log2(c / total) for c in counts.values())
    return round(value + 0.0, 2)

for text in ["aaaaaaaa", "password", "q8Zr2LxP0vT7mWk9", ""]:
    print(repr(text), entropy(text))
