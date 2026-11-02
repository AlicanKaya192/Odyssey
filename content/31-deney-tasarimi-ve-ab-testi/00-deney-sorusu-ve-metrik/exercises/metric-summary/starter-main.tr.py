from ab_data import make_user_log

users = make_user_log(n=5000, seed=711)
# Kullanıcı başına ortalamaları alt alta yazdır:
# bought (4 basamak), revenue (2 basamak), minutes (1 basamak).
