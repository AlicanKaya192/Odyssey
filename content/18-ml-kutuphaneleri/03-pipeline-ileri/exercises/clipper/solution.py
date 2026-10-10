import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Clipper(BaseEstimator, TransformerMixin):
    def __init__(self, high=0.99):
        self.high = high

    def fit(self, X, y=None):
        self.upper_ = np.quantile(np.asarray(X, dtype=float), self.high, axis=0)
        return self

    def transform(self, X):
        check_is_fitted(self)
        return np.minimum(np.asarray(X, dtype=float), self.upper_)


def clip_values(train, test, high):
    clip = Clipper(high=high).fit(train)
    return clip.transform(test).tolist()

print(clip_values([[1.0], [2.0], [3.0], [4.0], [100.0]], [[0.0], [50.0]], 0.75))
