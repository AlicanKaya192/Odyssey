import numpy as np


def top_rows(table, col, k):
    m = np.array(table)
    return m[:k].tolist()

table = [[3, 90], [1, 75], [2, 82], [4, 60]]
print(top_rows(table, 1, 2))
