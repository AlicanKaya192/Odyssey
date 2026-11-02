import numpy as np
from ab_data import make_population

users = make_population()
for col in ["load_ms", "minutes"]:
    x = users[col]
    print(col, round(x.mean(), 1))
# Her satıra ortalamanın yanına medyanı, standart sapmayı ve 95.
# yüzdeliği ekle (hepsi 1 basamak). Sonra ortalama ile medyanı en çok
# ayrışan sütunun adını yazdır.
