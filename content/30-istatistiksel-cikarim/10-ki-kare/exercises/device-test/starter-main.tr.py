import pandas as pd
from scipy import stats
from ab_data import make_devices

users = make_devices(n=2000, seed=162)
table = pd.crosstab(users["device"], users["bought"])
result = stats.chi2_contingency(table)
print(round(result.statistic, 2))
# Bu satıra serbestlik derecesini (result.dof) ve p'yi (4 basamak) ekle.
# Sonraki satırda Cramér's V (3 basamak):
# stats.contingency.association(table, method="cramer")
