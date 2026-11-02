import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


import numpy as np
from ab_data import make_user_log

ids = make_user_log(n=5000, seed=724)["user_id"]
first = np.array([bucket(u, "price-test") < 50 for u in ids])
second = np.array([bucket(u, "price-test") < 50 for u in ids])
print(round(float(np.mean(first == second)), 3))
