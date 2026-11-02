import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


import numpy as np
from ab_data import make_user_log

users = make_user_log(n=10000, seed=721)
# 1) "banner-test" tuzuyla kovası 50'den küçük olanları B say.
# 2) B'nin payını (3 basamak), sonra A'nın ve B'nin ortalama ziyaret
#    sayısını (sessions, 2 basamak) alt alta yazdır.
