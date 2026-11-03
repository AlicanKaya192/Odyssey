import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# Bu senaryoda B'nin etkisi yok (lift=0.0).
# 1) SRM p'sini (stats.chisquare) 3 basamakla yaz.
# 2) Satın alma farkının %95 aralığını (önce B) puan olarak 2 basamakla yaz.
