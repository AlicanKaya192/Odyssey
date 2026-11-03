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

# lift = 0.0 ve lift = 0.15 için make_experiment(n=10000, seed=s, lift=lift)
# ile s = 0..99 arası 100 test kur. Her lift için lift değerini ve
# analyse'ın kaç kez "ship" dediğini aynı satırda yaz.
