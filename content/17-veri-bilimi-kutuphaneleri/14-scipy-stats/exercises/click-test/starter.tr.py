import numpy as np
from scipy import stats


def click_test(table):
    res = stats.chi2_contingency(np.array(table))
    return {"stat": 0.0, "dof": 0, "significant": False, "expected": []}

result = click_test([[90, 60], [45, 105]])
print(result["stat"], result["dof"], result["significant"])
print(result["expected"])
