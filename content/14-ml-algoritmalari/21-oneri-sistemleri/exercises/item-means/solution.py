import numpy as np


def item_means(R):
    R = np.array(R, dtype=float)
    mask = R > 0
    mu = R[mask].mean()
    result = []
    for i in range(R.shape[1]):
        col = R[mask[:, i], i]
        result.append(round(float(col.mean()) if len(col) else float(mu), 2))
    return result

R = [[5, 0, 3], [4, 0, 0], [0, 0, 1], [3, 0, 2]]
print(item_means(R))
