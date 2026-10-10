import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(9)
days = rng.integers(10, 365, 500)
risk = rng.normal(0, 1, 500)
claims = rng.poisson(np.exp(-4 + 0.5 * risk) * days)
d3 = pd.DataFrame({"claims": claims, "risk": risk, "days": days})
def claim_model():
    res = smf.glm("claims ~ risk", data=d3, family=sm.families.Poisson()).fit()
    return [round(float(np.exp(res.params["risk"])), 3), round(float(res.params["Intercept"]), 3)]

print(claim_model())
