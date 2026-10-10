from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
from sklearn.feature_selection import SelectKBest, f_classif


def best_columns(k):
    kb = SelectKBest(f_classif, k=k).fit(X, y)
    return sorted(kb.get_support(indices=True).tolist())

print(best_columns(4))
print(best_columns(2))
