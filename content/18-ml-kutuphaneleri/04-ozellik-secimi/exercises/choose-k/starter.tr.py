from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline


def choose_k(ks):
    return {"scores": [], "best": None}

result = choose_k([2, 4, 20])
print(result["scores"])
print(result["best"])
