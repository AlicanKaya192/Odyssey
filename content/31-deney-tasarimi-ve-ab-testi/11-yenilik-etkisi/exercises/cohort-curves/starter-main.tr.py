from ab_data import make_novelty_test

clicks = make_novelty_test(n=10000, seed=12)
clicks["week"] = (clicks["day"] - 1) // 7 + 1
# Eski (is_new False) ve yeni (True) kullanıcılar için haftalık göreli
# artışları (B / A - 1, 3 basamak) liste olarak yaz: önce grubun değeri
# (False / True), sonra liste.
