from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=8, n_informative=4,
                           weights=[0.9], flip_y=0.02, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7,
                                                    stratify=y)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, make_scorer
from sklearn.model_selection import TunedThresholdClassifierCV


def cost(y_true, y_pred, fn_cost):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return int(fp + fn * fn_cost)


def tuned_threshold(fn_cost):
    scorer = make_scorer(cost, greater_is_better=False, fn_cost=fn_cost)
    tuned = TunedThresholdClassifierCV(LogisticRegression(), scoring=scorer, cv=5)
    tuned.fit(X_train, y_train)
    return [round(float(tuned.best_threshold_), 3), cost(y_test, tuned.predict(X_test), fn_cost)]

print(tuned_threshold(1))
print(tuned_threshold(10))
