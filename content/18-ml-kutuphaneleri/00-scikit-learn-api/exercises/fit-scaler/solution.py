import numpy as np
from sklearn.preprocessing import StandardScaler


def fit_scaler(train, test):
    scaler = StandardScaler().fit(np.array(train, dtype=float))
    return [scaler.mean_.round(3).tolist(), scaler.transform(np.array(test, dtype=float)).round(2).tolist()]

print(fit_scaler([[1.0, 10.0], [3.0, 30.0]], [[2.0, 50.0]]))
