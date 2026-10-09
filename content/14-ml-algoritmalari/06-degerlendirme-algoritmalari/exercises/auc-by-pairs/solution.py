import numpy as np


def auc_by_pairs(y, score):
    y, score = np.array(y), np.array(score, dtype=float)
    pos, neg = score[y == 1], score[y == 0]
    wins = (pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()
    return round(float(wins / (len(pos) * len(neg))), 4)

print(auc_by_pairs([1, 0, 1, 0], [0.9, 0.1, 0.4, 0.6]))
print(auc_by_pairs([1, 0], [0.5, 0.5]))
