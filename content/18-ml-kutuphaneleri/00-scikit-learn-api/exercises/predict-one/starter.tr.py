import numpy as np
from sklearn.linear_model import LinearRegression


def predict_one(xs, ys, x):
    model = LinearRegression().fit(np.array(xs), np.array(ys))
    return round(float(model.predict(np.array([x]))[0]), 2)

print(predict_one([1, 2, 3, 4], [3, 5, 7, 9], 10))
