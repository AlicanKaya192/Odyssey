from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=5000, n_features=20, n_informative=6,
                           flip_y=0.1, random_state=5)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5)
from lightgbm import LGBMClassifier

model = LGBMClassifier(random_state=0, verbose=-1).fit(X_train, y_train)


def gain_top(k):
    values = model.booster_.feature_importance(importance_type="gain")
    return values.argsort()[::-1][:k].tolist()

print(gain_top(3))
