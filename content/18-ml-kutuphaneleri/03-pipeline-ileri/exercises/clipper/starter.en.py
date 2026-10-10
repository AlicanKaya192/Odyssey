import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Clipper(BaseEstimator, TransformerMixin):
    pass


def clip_values(train, test, high):
    return []

print(clip_values([[1.0], [2.0], [3.0], [4.0], [100.0]], [[0.0], [50.0]], 0.75))
