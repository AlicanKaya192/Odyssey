import numpy as np
from ab_data import make_experiment

test = make_experiment(n=8000, seed=751)
buyers = test[test["bought"] == 1]
order_a = buyers.loc[buyers["group"] == "A", "revenue"].to_numpy()
order_b = buyers.loc[buyers["group"] == "B", "revenue"].to_numpy()
rng = np.random.default_rng(752)
# 1) 1000 kez: B'den sonra A'dan yerine koyarak örnekle, medyan farkını
#    (B - A) listeye ekle.
# 2) İki grubun medyanını, sonra farkın %95 aralığını 2 basamakla yaz.
