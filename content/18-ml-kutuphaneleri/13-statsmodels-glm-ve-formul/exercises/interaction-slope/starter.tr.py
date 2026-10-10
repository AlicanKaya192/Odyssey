import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(11)
df = pd.DataFrame({
    "area": rng.uniform(50, 200, 300).round(),
    "city": rng.choice(["Ankara", "Izmir", "Istanbul"], 300),
    "age": rng.uniform(0, 40, 300).round(),
})
bonus = df["city"].map({"Ankara": 0, "Izmir": 40, "Istanbul": 120})
df["price"] = 50 + 3 * df["area"] - 2 * df["age"] + bonus + rng.normal(0, 30, 300)
extra = 1.5 * df["area"] * (df["city"] == "Istanbul")
df["price2"] = 50 + 3 * df["area"] + extra - 2 * df["age"] + rng.normal(0, 30, 300)
def interaction_slope(city):
    res = smf.ols("price2 ~ area + C(city) + age", data=df).fit()
    return round(float(res.params[f"area:C(city)[T.{city}]"]), 2)

print(interaction_slope("Istanbul"))
print(interaction_slope("Izmir"))
