import statistics


def zscore_flags(baseline, values, limit):
    mean = statistics.mean(baseline)
    stdev = statistics.stdev(baseline)
    return [v for v in values if abs((v - mean) / stdev) > limit]

BASELINE = [120, 130, 125, 118, 122, 127, 131, 124]
print(zscore_flags(BASELINE, [126, 410, 100, 140], 3))
print(zscore_flags([5, 5, 5], [5, 6], 3))
