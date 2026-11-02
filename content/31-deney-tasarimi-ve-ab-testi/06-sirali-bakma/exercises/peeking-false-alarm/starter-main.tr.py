import numpy as np
from scipy import stats
from ab_data import make_experiment


def daily_p(test, days=14):
    is_b = (test["group"] == "B").to_numpy()
    day = test["day"].to_numpy()
    bought = test["bought"].to_numpy().astype(float)
    size = days + 1
    n_a = np.cumsum(np.bincount(day[~is_b], minlength=size))[1:]
    n_b = np.cumsum(np.bincount(day[is_b], minlength=size))[1:]
    k_a = np.cumsum(np.bincount(day[~is_b], bought[~is_b], size))[1:]
    k_b = np.cumsum(np.bincount(day[is_b], bought[is_b], size))[1:]
    pooled = (k_a + k_b) / (n_a + n_b)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (k_b / n_b - k_a / n_a) / se
    return 2 * stats.norm.sf(np.abs(z))


aa = np.array([daily_p(make_experiment(n=6000, seed=s, lift=0.0))
               for s in range(7000, 7200)])
# 200 A/A deneyinin günlük p'leri aa'da (satır = deney, sütun = gün).
# Yanlış alarm oranını iki biçimde 3 basamakla yaz:
# 1) yalnızca son gün bakılınca, 2) her gün bakılınca (en küçük p).
