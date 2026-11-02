import numpy as np
from ab_data import make_population

users = make_population()
true_mean = users["minutes"].mean()
sample = users["minutes"].sample(n=50, random_state=0)
print(round(sample.mean(), 2))
# Tek örneklem yetmez: bunu seed 0..499 için tekrarla, ortalamaları
# bir listede topla ve en küçüğü, en büyüğü ve gerçeğe 1 dakikadan
# yakın olanların payını yazdır.
