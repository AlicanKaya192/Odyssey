import math
from collections import Counter


def entropy(text):
    counts = Counter(text)
    # her karakterin orani p: -sum(p * log2(p))
    return 0.0

for text in ["aaaaaaaa", "password", "q8Zr2LxP0vT7mWk9", ""]:
    print(repr(text), entropy(text))
