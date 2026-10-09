import numpy as np


def rmse(y_true, y_pred):
    t, p = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    # sqrt(mean(squared difference))
    return 0.0

print(rmse([4, 3, 5, 2], [3.5, 3, 4, 2.5]))
print(rmse([1, 5], [5, 1]))
