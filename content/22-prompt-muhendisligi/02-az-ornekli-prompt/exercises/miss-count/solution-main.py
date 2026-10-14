import random

from shop_data import TICKETS, LABELS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def miss_count(k, draws):
    missing = 0
    for seed in range(draws):
        picked = random.Random(seed).sample(POOL, k)
        if len({t["label"] for t in picked}) < len(LABELS):
            missing += 1
    return missing


for k in [5, 10, 15]:
    print(k, miss_count(k, 1000))
