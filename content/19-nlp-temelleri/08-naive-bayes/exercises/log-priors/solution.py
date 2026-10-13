import math
from collections import Counter


def log_priors(labels):
    counts = Counter(labels)
    return {c: round(math.log(counts[c] / len(labels)), 3) for c in sorted(counts)}

print(log_priors(["pos", "pos", "neg", "pos"]))
