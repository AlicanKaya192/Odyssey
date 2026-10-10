from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=8, n_informative=4,
                           weights=[0.9], flip_y=0.02, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7,
                                                    stratify=y)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def auc_score(c):
    model = LogisticRegression(C=c).fit(X_train, y_train)
    return round(float(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])), 3)

print(auc_score(1.0))
print(auc_score(0.01))
