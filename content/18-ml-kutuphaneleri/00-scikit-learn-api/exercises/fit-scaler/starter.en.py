import numpy as np
from sklearn.preprocessing import StandardScaler


def fit_scaler(train, test):
    scaler = StandardScaler().fit(np.vstack([train, test]))
    return [scaler.mean_.round(3).tolist(), scaler.transform(test).round(2).tolist()]

print(fit_scaler([[1.0, 10.0], [3.0, 30.0]], [[2.0, 50.0]]))
