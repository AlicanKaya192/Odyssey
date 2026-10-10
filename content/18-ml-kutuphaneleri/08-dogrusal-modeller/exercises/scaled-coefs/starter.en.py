import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
area = rng.uniform(50, 200, 300)
rooms = rng.integers(1, 6, 300)
age = rng.uniform(0, 40, 300)
price = 3 * area + 20 * rooms - 2 * age + rng.normal(0, 30, 300)
data = pd.DataFrame({"area": area, "rooms": rooms, "age": age})
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def scaled_coefs(columns):
    model = LinearRegression().fit(data[columns], price)
    return [round(float(v), 1) for v in model.coef_]

print(scaled_coefs(["area", "rooms", "age"]))
print(scaled_coefs(["age", "rooms"]))
