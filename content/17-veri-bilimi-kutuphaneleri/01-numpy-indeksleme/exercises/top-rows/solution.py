import numpy as np


def top_rows(table, col, k):
    m = np.array(table)
    order = m[:, col].argsort()[::-1]
    return m[order][:k].tolist()

table = [[3, 90], [1, 75], [2, 82], [4, 60]]
print(top_rows(table, 1, 2))
