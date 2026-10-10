import numpy as np
from scipy import stats


def ab_report(a, b):
    res = stats.ttest_ind(b, a, equal_var=False)
    low, high = res.confidence_interval()
    if low > 0:
        decision = "b better"
    elif high < 0:
        decision = "a better"
    else:
        decision = "unclear"
    diff = round(float(np.mean(b) - np.mean(a)), 2)
    return {"diff": diff, "interval": [round(float(low), 2), round(float(high), 2)], "decision": decision}

A = [52.1, 48.3, 55.0, 61.2, 47.5, 50.8, 58.9, 44.2, 53.7, 49.9]
B = [60.4, 71.8, 45.2, 80.1, 66.3, 52.7, 77.9, 58.0]
result = ab_report(A, B)
print(result["diff"], result["interval"])
print(result["decision"])
