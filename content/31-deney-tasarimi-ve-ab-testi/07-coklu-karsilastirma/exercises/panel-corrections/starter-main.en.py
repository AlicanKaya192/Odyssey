import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ab_data import make_metric_panel

panel = make_metric_panel(n=6000, seed=12)
metrics = [c for c in panel.columns if c.startswith("metric_")]
values = panel[metrics].to_numpy()
is_b = (panel["group"] == "B").to_numpy()
# 1) Compute the Welch ps of the 20 metrics (stats.ttest_ind, equal_var=False).
# 2) Print the number of metrics with p < 0.05.
# 3) For "holm" and "fdr_bh", print the method name and the accepted count.
