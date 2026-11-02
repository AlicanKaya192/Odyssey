import pandas as pd
from scipy import stats
from ab_data import make_devices

users = make_devices(n=2000, seed=162)
table = pd.crosstab(users["device"], users["bought"])
result = stats.chi2_contingency(table)
print(round(result.statistic, 2))
# Add the degrees of freedom (result.dof) and p (4 places) to this line.
# On the next line, Cramer's V (3 places):
# stats.contingency.association(table, method="cramer")
