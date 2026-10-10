import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
def effect(column):
    res = sm.OLS(price, X).fit()
    low, high = res.conf_int().loc[column]
    values = [res.params[column], res.pvalues[column], low, high]
    return [round(float(v), 3) for v in values]

print(effect("area"))
print(effect("noise"))
