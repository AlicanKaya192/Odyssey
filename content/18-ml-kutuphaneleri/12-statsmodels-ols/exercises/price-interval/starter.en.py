import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
res = sm.OLS(price, sm.add_constant(X)).fit()


def price_interval(area, age):
    new = pd.DataFrame({"area": [area], "age": [age], "noise": [0.0]})
    frame = res.get_prediction(sm.add_constant(new)).summary_frame(alpha=0.05)
    row = frame.iloc[0]
    return [round(float(row["mean"]), 1), round(float(row["obs_ci_lower"]), 1),
            round(float(row["obs_ci_upper"]), 1)]

print(price_interval(100, 10))
