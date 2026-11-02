import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_experiment

test = make_experiment(n=6000, seed=753)
labels = (test["group"] == "B").to_numpy()
bought = test["bought"].to_numpy()
rng = np.random.default_rng(754)
observed = bought[labels].mean() - bought[~labels].mean()
# 1) 2000 kez etiketleri karıştır (rng.permutation(labels)), farkı
#    hesapla; mutlak değeri gerçek farktan büyük ya da eşitse say.
# 2) Permütasyon p'sini, sonra iki oran z-testinin p'sini 3 basamakla yaz.
