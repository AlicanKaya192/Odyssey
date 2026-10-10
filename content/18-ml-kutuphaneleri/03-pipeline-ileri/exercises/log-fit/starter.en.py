import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer


def log_fit(xs, ys, x):
    X = np.array(xs, dtype=float).reshape(-1, 1)
    model = LinearRegression().fit(X, ys)
    return round(float(model.predict([[x]])[0]), 2)

print(log_fit([1.0, 10.0, 100.0, 1000.0], [1.0, 2.0, 3.0, 4.0], 10000.0))
