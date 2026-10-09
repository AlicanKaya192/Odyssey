import numpy as np


def transition_matrix(links):
    n = len(links)
    M = np.zeros((n, n))
    # Her j sutunu: baglantilara 1/cikis, yoksa 1/n
    return M.round(3).tolist()

links = [[1, 2], [2], [0]]
for row in transition_matrix(links):
    print(row)
