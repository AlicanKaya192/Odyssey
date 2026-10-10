from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)
Xs = StandardScaler().fit_transform(X)
from sklearn.linear_model import LogisticRegression


def l1_counts(c):
    model = LogisticRegression(C=c, max_iter=5000).fit(Xs, y)
    return (model.coef_ != 0).sum(axis=1).tolist()

print(l1_counts(1))
print(l1_counts(0.1))
