from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_ramp_test

ramp = make_ramp_test(seed=11)
pooled = ramp.groupby("group")["bought"].mean()
print(round(float(pooled["A"]), 4), round(float(pooled["B"]), 4))
week2 = ramp[ramp["week"] == 2]
rates = week2.groupby("group")["bought"].mean()
print(round(float(rates["A"]), 4), round(float(rates["B"]), 4))
k = week2.groupby("group")["bought"].sum()
n = week2.groupby("group").size()
print(round(float(proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]), 3))
