import numpy as np
from sklearn.feature_selection import VarianceThreshold


def non_constant(rows):
    X = np.array(rows, dtype=float)
    vt = VarianceThreshold(threshold=0).fit(X)
    return vt.get_support(indices=True).tolist()

print(non_constant([[0, 1.0, 5.0], [0, 2.0, 5.0], [0, 3.0, 5.0]]))
