import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(4)
score = rng.normal(0, 1, 1000)
premium = rng.integers(0, 2, 1000)
chance = 1 / (1 + np.exp(-(-1 + 0.8 * score + 1.2 * premium)))
d2 = pd.DataFrame({"y": (rng.random(1000) < chance).astype(int),
                   "score": score, "premium": premium})
def odds_ratio(column):
    res = smf.logit("y ~ score + premium", data=d2).fit(disp=0)
    return round(float(res.params[column]), 2)

print(odds_ratio("score"))
print(odds_ratio("premium"))
