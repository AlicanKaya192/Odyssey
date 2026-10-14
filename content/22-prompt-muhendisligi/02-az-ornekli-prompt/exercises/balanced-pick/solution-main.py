import random

from shop_data import TICKETS, LABELS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def balanced_ids(per_label, seed):
    rng = random.Random(seed)
    chosen = []
    for label in LABELS:
        same = [t for t in POOL if t["label"] == label]
        chosen += rng.sample(same, per_label)
    rng.shuffle(chosen)
    return [t["id"] for t in chosen]


print(balanced_ids(1, 3))
print(len(balanced_ids(2, 0)))
