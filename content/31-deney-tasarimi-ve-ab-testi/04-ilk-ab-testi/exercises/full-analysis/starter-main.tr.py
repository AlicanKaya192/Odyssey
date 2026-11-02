from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment


def decide(srm_p, low, threshold):
    if srm_p < 0.001:
        return "stop: SRM"
    if low >= threshold:
        return "ship"
    if low > 0:
        return "unclear"
    return "no evidence"


test = make_experiment(n=20000, seed=743, lift=0.15)
n = test["group"].value_counts().sort_index()
k = test.groupby("group")["bought"].sum()
# 1) SRM p'sini (stats.chisquare) 3 basamakla yaz.
# 2) B - A farkının %95 aralığını 4 basamakla yaz.
# 3) decide(srm_p, low, 0.003) sonucunu yaz.
