from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_checkout_test


def decide(low, high, threshold):
    if low >= threshold:
        return "apply"
    if high < threshold:
        return "skip"
    return "unclear"


shop = make_checkout_test(n=8000, seed=312)
buy_a = shop.loc[shop["group"] == "A", "bought"].sum()
buy_b = shop.loc[shop["group"] == "B", "bought"].sum()
low, high = confint_proportions_2indep(buy_b, 8000, buy_a, 8000)
print(round(low, 4), round(high, 4))
print(decide(low, high, 0.01))
