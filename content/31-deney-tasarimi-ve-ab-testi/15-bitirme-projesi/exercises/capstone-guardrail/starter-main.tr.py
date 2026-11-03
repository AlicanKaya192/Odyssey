import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# Alıcılarda iade oranı farkının (önce B) %95 aralığını hesapla.
# 1) Üst ucu puan olarak 2 basamakla yaz.
# 2) Üst uç 2 puanın (0.02) altında mı? True / False yaz.
