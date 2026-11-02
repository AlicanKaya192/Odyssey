import pandas as pd
from scipy import stats
from ab_data import make_devices

users = make_devices(n=2000, seed=162)
table = pd.crosstab(users["device"], users["bought"])
result = stats.chi2_contingency(table)
v = stats.contingency.association(table, method="cramer")
print(round(result.statistic, 2), result.dof, round(result.pvalue, 4))
print(round(float(v), 3))
