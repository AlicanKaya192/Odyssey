import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# Gelir için CUPED uygula (ortak değişken pre_spend).
# 1) pre_spend ile revenue korelasyonunu 2 basamakla yaz.
# 2) Kalan varyans oranını (düzeltilmiş / ham) 3 basamakla yaz.
