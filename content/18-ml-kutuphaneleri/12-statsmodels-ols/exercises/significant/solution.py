import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
def significant(alpha):
    res = sm.OLS(price, sm.add_constant(X)).fit()
    return [name for name in res.pvalues.index
            if name != "const" and res.pvalues[name] < alpha]

print(significant(0.05))
print(significant(0.3))
