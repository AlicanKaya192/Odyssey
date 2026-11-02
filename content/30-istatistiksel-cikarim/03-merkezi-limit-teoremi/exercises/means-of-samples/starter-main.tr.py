import numpy as np
from ab_data import make_population

users = make_population()
x = users["minutes"].to_numpy()
rng = np.random.default_rng(11)
means = rng.choice(x, size=(3000, 4)).mean(axis=1)
print(4, round(means.mean(), 2))
# Bunu n = 4 ve n = 64 için bir döngüde yap. Her satıra n'den sonra
# ortalamaların ortalamasını (2 basamak), ortalamaların standart
# sapmasını (3 basamak) ve x.std() / np.sqrt(n) formülünü (3 basamak) yaz.
