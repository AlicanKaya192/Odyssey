from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=10, n_informative=4,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def pipe_search(ks, cs):
    pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif), LogisticRegression())
    search = GridSearchCV(pipe, {"k": ks, "C": cs}, cv=5).fit(X_train, y_train)
    best = search.best_params_
    return {"params": [best["k"], best["C"]], "test": round(search.score(X_test, y_test), 3)}

result = pipe_search([2, 4, 8], [0.1, 1.0])
print(result["params"])
print(result["test"])
