import numpy as np
from scipy import stats


def click_test(table):
    res = stats.chi2_contingency(np.array(table))
    return {"stat": round(float(res.statistic), 2), "dof": int(res.dof),
            "significant": bool(res.pvalue < 0.05),
            "expected": res.expected_freq.round(1).tolist()}

result = click_test([[90, 60], [45, 105]])
print(result["stat"], result["dof"], result["significant"])
print(result["expected"])
