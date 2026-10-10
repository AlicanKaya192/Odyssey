import numpy as np
import pandas as pd


def discounts(qtys):
    q = pd.Series(qtys)
    rate = np.select([q >= 25, q >= 10], [0.2, 0.1], default=0.0)
    return rate.tolist()

print(discounts([1, 12, 5, 30, 25]))
