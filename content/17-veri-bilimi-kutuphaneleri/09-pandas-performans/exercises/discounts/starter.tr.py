import numpy as np
import pandas as pd


def discounts(qtys):
    q = pd.Series(qtys)
    rate = np.select([q >= 10, q >= 25], [0.1, 0.2], default=0.0)
    return rate.tolist()

print(discounts([1, 12, 5, 30, 25]))
