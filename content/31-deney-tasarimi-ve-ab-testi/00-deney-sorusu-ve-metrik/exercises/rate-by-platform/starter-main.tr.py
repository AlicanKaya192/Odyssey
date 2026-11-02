from ab_data import make_user_log

users = make_user_log(n=8000, seed=713)
# Platforma göre satın alma oranını bul (groupby). Alt alta yazdır:
# masaüstü, mobil ve farkları (masaüstü - mobil), 4 basamak.
