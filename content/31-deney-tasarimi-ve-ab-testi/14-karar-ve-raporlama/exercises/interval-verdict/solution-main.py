from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

test = make_experiment(n=12000, seed=46, lift=0.1)


def verdict(low, high, threshold=0.003):
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


k = test.groupby("group")["bought"].sum()
n = test.groupby("group").size()
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print(round(low * 100, 2), round(high * 100, 2))
print(verdict(low, high))
