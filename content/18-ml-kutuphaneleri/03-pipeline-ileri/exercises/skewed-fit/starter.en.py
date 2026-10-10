import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def skewed_fit(seed):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 3, size=(300, 1))
    y = np.exp(1.0 + 1.2 * X[:, 0] + rng.normal(0, 0.3, 300))
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    model = LinearRegression().fit(X_train, y_train)
    return [round(model.score(X_test, y_test), 2), round(float(model.predict([[0.0]])[0]), 2)]

print(skewed_fit(7))
