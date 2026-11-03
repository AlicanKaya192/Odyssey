import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=84, lift=0.06)
# Bu projede B'nin gerçek etkisi %6 (göreli).
# 1) SRM p'sini 3 basamakla yaz.
# 2) Satın alma farkının %95 aralığını (önce B) puan olarak 2 basamakla yaz.
# 3) Gelir için CUPED'den sonra kalan varyansı (1 - rho ** 2; rho, pre_spend
#    ile revenue korelasyonu) 3 basamakla yaz.
