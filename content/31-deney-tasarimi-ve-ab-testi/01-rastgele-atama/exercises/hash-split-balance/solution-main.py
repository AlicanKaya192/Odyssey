import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


import numpy as np
from ab_data import make_user_log

users = make_user_log(n=10000, seed=721)
in_b = np.array([bucket(u, "banner-test") < 50 for u in users["user_id"]])
print(round(float(in_b.mean()), 3))
print(round(users["sessions"][~in_b].mean(), 2))
print(round(users["sessions"][in_b].mean(), 2))
