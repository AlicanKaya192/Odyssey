from sklearn.datasets import make_regression

X, y = make_regression(n_samples=200, n_features=4, noise=20, random_state=1)
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score


def positive_mae(alpha):
    scores = cross_val_score(Ridge(alpha=alpha), X, y, cv=5,
                             scoring="neg_mean_absolute_error")
    return round(float(-scores.mean()), 2)

print(positive_mae(1.0))
print(positive_mae(100.0))
