import numpy as np
from sklearn.impute import SimpleImputer


def fill_median(rows):
    X = np.array(rows, dtype=float)
    return SimpleImputer(strategy="mean").fit_transform(X).round(2).tolist()

print(*fill_median([[1.0, 7.0], [None, 8.0], [3.0, None], [100.0, 9.0]]), sep="\n")
