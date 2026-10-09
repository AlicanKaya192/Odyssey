def percentile(values, q):
    s = sorted(values)
    pos = (len(s) - 1) * q / 100
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (pos - lo), 2)

data = [7, 1, 3, 9, 4, 6, 2]
for q in (0, 25, 50, 90, 100):
    print(q, percentile(data, q))
