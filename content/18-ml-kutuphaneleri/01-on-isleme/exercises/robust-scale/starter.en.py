import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler


def robust_scale(values):
    X = np.array(values, dtype=float).reshape(-1, 1)
    return StandardScaler().fit_transform(X).ravel().round(2).tolist()

print(robust_scale([30, 35, 40, 45, 500]))
