import random

from shop_data import TICKETS, LABELS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def miss_count(k, draws):
    return 0


for k in [5, 10, 15]:
    print(k, miss_count(k, 1000))
