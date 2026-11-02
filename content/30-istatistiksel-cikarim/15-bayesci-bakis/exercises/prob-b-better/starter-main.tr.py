import numpy as np
from ab_data import make_checkout_test

shop = make_checkout_test(n=1500, seed=511)
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
rng = np.random.default_rng(512)
# 1) Düz önselle iki sonsaldan 100_000'er örnek çek (önce A, sonra B).
# 2) P(B > A)'yı 3 basamakla yazdır.
# 3) Farkın (B - A) %95 inandırıcı aralığını 4 basamakla yazdır.
