from sklearn.datasets import make_regression

X, y = make_regression(n_samples=200, n_features=30, n_informative=5,
                       noise=10, random_state=5)
import numpy as np
from sklearn.linear_model import Lasso


def lasso_columns(alpha):
    model = Lasso(alpha=alpha).fit(X, y)
    return int((model.coef_ > 0).sum())

print(lasso_columns(5))
print(len(lasso_columns(1)))
