from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=8, n_informative=4,
                           weights=[0.9], flip_y=0.02, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7,
                                                    stratify=y)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, make_scorer
from sklearn.model_selection import cross_val_score


def mean_cost(fn_cost, weight):
    def cost(y_true, y_pred):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return int(fp + fn * fn_cost)

    scorer = make_scorer(cost, greater_is_better=False)
    model = LogisticRegression(class_weight=weight)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring=scorer)
    return round(float(-scores.mean()), 1)

print(mean_cost(10, None))
print(mean_cost(10, "balanced"))
