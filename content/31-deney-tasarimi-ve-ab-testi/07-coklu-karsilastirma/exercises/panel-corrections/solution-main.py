import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ab_data import make_metric_panel

panel = make_metric_panel(n=6000, seed=12)
metrics = [c for c in panel.columns if c.startswith("metric_")]
values = panel[metrics].to_numpy()
is_b = (panel["group"] == "B").to_numpy()
p = stats.ttest_ind(values[is_b], values[~is_b], equal_var=False).pvalue
print(int((p < 0.05).sum()))
for method in ["holm", "fdr_bh"]:
    reject = multipletests(p, alpha=0.05, method=method)[0]
    print(method, int(reject.sum()))
