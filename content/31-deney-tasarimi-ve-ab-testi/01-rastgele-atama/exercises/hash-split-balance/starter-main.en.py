import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


import numpy as np
from ab_data import make_user_log

users = make_user_log(n=10000, seed=721)
# 1) With the salt "banner-test", count users with bucket below 50 as B.
# 2) Print B's share (3 places), then the mean sessions of A and of B
#    (2 places), one per line.
