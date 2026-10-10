from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=5000, n_features=20, n_informative=6,
                           flip_y=0.1, random_state=5)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5)
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV


def leaves_search(options):
    model = LGBMClassifier(n_estimators=100, random_state=0, verbose=-1)
    search = GridSearchCV(model, {"num_leaves": options}, cv=3).fit(X_train, y_train)
    return [search.best_params_["num_leaves"], round(float(search.best_score_), 3)]

print(leaves_search([4, 15, 63]))
