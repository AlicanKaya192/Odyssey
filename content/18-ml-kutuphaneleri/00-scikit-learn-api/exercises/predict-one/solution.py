import numpy as np
from sklearn.linear_model import LinearRegression


def predict_one(xs, ys, x):
    X = np.array(xs, dtype=float).reshape(-1, 1)
    model = LinearRegression().fit(X, np.array(ys, dtype=float))
    return round(float(model.predict([[x]])[0]), 2)

print(predict_one([1, 2, 3, 4], [3, 5, 7, 9], 10))
