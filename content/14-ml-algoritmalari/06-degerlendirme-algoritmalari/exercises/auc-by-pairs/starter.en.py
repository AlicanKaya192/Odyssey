import numpy as np


def auc_by_pairs(y, score):
    y, score = np.array(y), np.array(score, dtype=float)
    pos, neg = score[y == 1], score[y == 0]
    # All pairs: 1 if higher, 0.5 if equal.
    return 0.0

print(auc_by_pairs([1, 0, 1, 0], [0.9, 0.1, 0.4, 0.6]))
print(auc_by_pairs([1, 0], [0.5, 0.5]))
