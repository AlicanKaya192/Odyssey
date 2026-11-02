from ab_data import make_population

users = make_population()
# Yalnızca en az 5 kez gelenleri seç (visits >= 5).
# 1) Bu grubun kullanıcılar içindeki payı (3 basamak)
# 2) Bütün kullanıcıların ortalama "minutes" değeri (2 basamak)
# 3) Bu grubun ortalama "minutes" değeri (2 basamak)
# 4) Aradaki fark: grup eksi herkes (2 basamak)
