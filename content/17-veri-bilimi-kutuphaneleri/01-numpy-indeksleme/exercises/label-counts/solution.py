import numpy as np


def label_counts(labels):
    values, counts = np.unique(np.array(labels), return_counts=True)
    return {str(v): int(c) for v, c in zip(values, counts)}

print(label_counts(["b", "a", "b", "c", "b"]))
