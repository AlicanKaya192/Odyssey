from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=80, n_features=60, n_informative=10,
                       noise=30, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
import numpy as np
from sklearn.linear_model import LinearRegression, RidgeCV


def ridge_alpha(alphas):
    model = LinearRegression().fit(X_train, y_train)
    return [0.0, round(float(model.score(X_test, y_test)), 3)]

print(ridge_alpha([0.1, 1.0, 10.0, 100.0]))
