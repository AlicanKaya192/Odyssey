import random

from shop_data import TICKETS, LABELS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def balanced_ids(per_label, seed):
    return []


print(balanced_ids(1, 3))
print(len(balanced_ids(2, 0)))
