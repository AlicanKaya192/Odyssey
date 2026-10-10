import pandas as pd
from sklearn.preprocessing import TargetEncoder


def target_codes(shops, bought, new_shops):
    enc = TargetEncoder(random_state=0)
    enc.fit(pd.DataFrame({"shop": shops}), bought)
    codes = enc.transform(pd.DataFrame({"shop": new_shops}))
    return codes.ravel().round(3).tolist()

SHOPS = ["a", "a", "a", "b", "b", "c", "c", "c", "c", "d"]
BOUGHT = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1]
print(target_codes(SHOPS, BOUGHT, ["a", "c", "z"]))
