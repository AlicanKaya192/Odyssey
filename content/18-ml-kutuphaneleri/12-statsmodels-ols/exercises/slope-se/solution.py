import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(3)
area = rng.lognormal(4.3, 0.5, 200)
y = 50 + 3 * area + rng.normal(0, 1, 200) * area ** 1.5 * 0.05
X = sm.add_constant(area)
def slope_se(kind):
    res = sm.OLS(y, X).fit(cov_type=kind)
    return round(float(res.bse[1]), 3)

print(slope_se("nonrobust"))
print(slope_se("HC3"))
