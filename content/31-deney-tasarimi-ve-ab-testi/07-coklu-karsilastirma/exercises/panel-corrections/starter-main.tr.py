import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ab_data import make_metric_panel

panel = make_metric_panel(n=6000, seed=12)
metrics = [c for c in panel.columns if c.startswith("metric_")]
values = panel[metrics].to_numpy()
is_b = (panel["group"] == "B").to_numpy()
# 1) 20 metriğin Welch p'lerini hesapla (stats.ttest_ind, equal_var=False).
# 2) p < 0.05 olan metrik sayısını yaz.
# 3) "holm" ve "fdr_bh" için yöntemin adını ve kabul edilen sayıyı yaz.
