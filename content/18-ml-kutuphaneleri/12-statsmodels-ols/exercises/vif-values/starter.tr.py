import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
X["twin"] = area * 0.09 + rng.normal(0, 0.5, 120)
from statsmodels.stats.outliers_influence import variance_inflation_factor


def vif_values(columns):
    data = X[columns].values
    return [round(float(variance_inflation_factor(data, i)), 1) for i in range(len(columns))]

print(vif_values(["area", "twin", "age"]))
print(vif_values(["area", "age"]))
