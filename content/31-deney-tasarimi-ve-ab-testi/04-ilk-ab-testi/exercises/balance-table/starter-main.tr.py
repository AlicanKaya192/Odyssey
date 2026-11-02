from ab_data import make_experiment

test = make_experiment(n=12000, seed=741)
test["mobile"] = (test["platform"] == "mobile").astype(int)
# Gruplara göre sessions ve mobile ortalamalarını bul (groupby).
# İlk satıra A ve B'nin sessions ortalamasını, ikinci satıra mobil
# paylarını 3 basamakla yazdır.
