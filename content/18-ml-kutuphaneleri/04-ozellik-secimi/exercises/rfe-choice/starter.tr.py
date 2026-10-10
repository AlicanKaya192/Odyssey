from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression


def rfe_choice():
    return [0, []]

print(rfe_choice())
