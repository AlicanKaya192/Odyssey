import pandas as pd
from sklearn.preprocessing import TargetEncoder


def target_codes(shops, bought, new_shops):
    means = pd.Series(bought).groupby(pd.Series(shops)).mean()
    return pd.Series(new_shops).map(means).round(3).tolist()

SHOPS = ["a", "a", "a", "b", "b", "c", "c", "c", "c", "d"]
BOUGHT = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1]
print(target_codes(SHOPS, BOUGHT, ["a", "c", "z"]))
