import numpy as np


def transition_matrix(links):
    n = len(links)
    M = np.zeros((n, n))
    # Each column j: 1/outdegree to links, else 1/n
    return M.round(3).tolist()

links = [[1, 2], [2], [0]]
for row in transition_matrix(links):
    print(row)
