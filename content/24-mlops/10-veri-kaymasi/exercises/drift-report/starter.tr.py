import bisect
import math


def drift_report(reference, current, columns, bins):
    # Her sutun icin: sinirlar, paylar, PSI, etiket.
    pass


reference = [{"fee": f, "calls": c} for f, c in zip(range(20, 40), [0, 1] * 10)]
current = [{"fee": f + 8, "calls": c} for f, c in zip(range(20, 40), [0, 1] * 10)]
for row in drift_report(reference, current, ["fee", "calls"], 4):
    print(row)
