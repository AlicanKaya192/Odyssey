from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment


def analyse(test, threshold=0.003):
    n = test.groupby("group").size()
    if stats.chisquare(n).pvalue < 0.001:
        return "stop: SRM"
    k = test.groupby("group")["bought"].sum()
    low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"

# For lift = 0.0 and lift = 0.15 build 100 tests with
# make_experiment(n=10000, seed=s, lift=lift), s = 0..99. For each lift
# print the lift value and how many times analyse said "ship" on one line.
