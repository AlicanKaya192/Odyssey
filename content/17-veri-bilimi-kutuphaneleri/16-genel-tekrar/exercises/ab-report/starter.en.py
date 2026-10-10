import numpy as np
from scipy import stats


def ab_report(a, b):
    return {"diff": 0.0, "interval": [0.0, 0.0], "decision": "unclear"}

A = [52.1, 48.3, 55.0, 61.2, 47.5, 50.8, 58.9, 44.2, 53.7, 49.9]
B = [60.4, 71.8, 45.2, 80.1, 66.3, 52.7, 77.9, 58.0]
result = ab_report(A, B)
print(result["diff"], result["interval"])
print(result["decision"])
