import numpy as np


def transition_matrix(links):
    n = len(links)
    M = np.zeros((n, n))
    for j in range(n):
        outs = links[j]
        if outs:
            for i in outs:
                M[i, j] = 1 / len(outs)
        else:
            M[:, j] = 1 / n
    return M.round(3).tolist()

links = [[1, 2], [2], [0]]
for row in transition_matrix(links):
    print(row)
