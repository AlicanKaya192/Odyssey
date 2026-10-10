from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=3000, n_features=20, n_informative=6,
                           flip_y=0.2, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25,
                                              random_state=3)
import lightgbm as lgb
from lightgbm import LGBMClassifier


def lgbm_early(patience):
    model = LGBMClassifier(n_estimators=2000, learning_rate=0.05, random_state=0, verbose=-1)
    model.fit(X_fit, y_fit, eval_X=X_val, eval_y=y_val,
              callbacks=[lgb.early_stopping(patience, verbose=False)])
    return [int(model.best_iteration_), round(float(model.score(X_test, y_test)), 3)]

print(lgbm_early(50))
print(lgbm_early(10))
