from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

test = make_experiment(n=12000, seed=46, lift=0.1)
k = test.groupby("group")["bought"].sum()
n = test.groupby("group").size()
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
rate_a, rate_b = k["A"] / n["A"], k["B"] / n["B"]
# Raporu kartın biçiminde, üç satırda yaz:
#   A 11.99% -> B 13.76%: +1.77 pts
#   95% CI 1.01 to 2.53
#   relative +14.8%
