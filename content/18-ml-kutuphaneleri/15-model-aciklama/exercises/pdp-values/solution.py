import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
df = pd.DataFrame({
    "area": rng.uniform(40, 200, 2000),
    "age": rng.uniform(0, 50, 2000),
    "floor": rng.integers(0, 15, 2000),
    "row_id": rng.permutation(2000),
    "coin": rng.integers(0, 2, 2000),
})
df["price"] = (df["area"] - 0.1 * (df["age"] - 25) ** 2
               + 8 * np.minimum(df["floor"], 8) + rng.normal(0, 15, 2000))
X, y = df.drop(columns="price"), df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
rf = RandomForestRegressor(n_estimators=100, random_state=0).fit(X_train, y_train)
from sklearn.inspection import partial_dependence


def pdp_values(column, points):
    result = partial_dependence(rf, X_test.astype({column: float}), [column],
                                grid_resolution=points)
    return result["average"][0].round().astype(int).tolist()

print(pdp_values("floor", 5))
print(pdp_values("age", 4))
